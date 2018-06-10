"""IPython extensions to display dot and provn files"""
import subprocess
import platform
import errno
import sys
import os
import tempfile
from collections import OrderedDict, deque

from IPython.display import display, Image, SVG
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.utils.text import DollarFormatter

from .view.dot import graph

LOADED = False

MIME_MAP = {
    # png
    "png": "image/png",
    "image/png": "image/png",
    # svg
    "svg": "image/svg+xml",
    "image/svg+xml": "image/svg+xml",
    # pdf
    "dot.pdf": "application/pdf",
    "ink.pdf": "application/pdf",
    "pdf": "application/pdf",
    "application/pdf": "application/pdf",
    # txt
    "txt": "text/plain",
    "text/plain": "text/plain",
    # dot
    "dot": "text/vnd.graphviz",
    "text/vnd.graphviz": "text/vnd.graphviz",
}


STARTUPINFO = None

if platform.system().lower() == 'windows':
    STARTUPINFO = subprocess.STARTUPINFO()
    STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    STARTUPINFO.wShowWindow = subprocess.SW_HIDE


def configure_graph(graph, args, cell):
    graph.reset_config()

    graph.size_x = args.width
    graph.size_y = args.height
    graph.rankdir = args.rankdir
    graph.set_style(args.style)
    # Dot header
    pos = cell.find("##H##")
    if pos != -1:
        graph.header = cell[:pos]
        cell = cell[pos+5:]

    # Dot footer
    pos = cell.find("##F##")
    if pos != -1:
        graph.footer = cell[pos + 5:]
        cell = cell[:pos]
    return cell, graph.generate(cell)


def run_dot(dot, ext="svg", prog="dot", extra=None):
    """Run graphviz for `dot` text and returns its output"""
    extra = extra or []
    args = [prog] + extra + ['-T', ext]
    process = subprocess.Popen(
        args, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        startupinfo=STARTUPINFO
    )
    try:
        tout, terr = process.communicate(dot.encode('utf-8'))
    except (OSError, IOError) as err:
        if err.errno != errno.ENOENT:
            raise
        # Get error message
        tout, terr = process.stdout.read(), process.stderr.read()
        process.wait()
    process.terminate()
    if process.returncode != 0:
        if terr is None:
            terr = b"Incomplete input"
        raise RuntimeError(
            'dot exited with error code {0}\n{1}'
            .format(process.returncode, terr.decode('utf-8'))
        )
    return tout


def dot_to_pdf(dot, prog, extra, force_ink=False):
    """Convert dot to pdf.
    First try to use graphviz (dot -> svg) and inkscape (svg -> pdf).
    If it fails, use graphviz (dot -> pdf)"""

    try:
        svg_text = run_dot(dot, "svg", prog, extra)
        if svg_text is None:
            raise RuntimeError("Invalid svg")
    except (OSError, IOError, RuntimeError):
        if force_ink:
            raise
        return run_dot(dot, "pdf", prog, extra)

    fd1, filename1 = tempfile.mkstemp()
    fd2, filename2 = tempfile.mkstemp()
    try:
        os.write(fd1, svg_text)
        os.close(fd1)
        os.close(fd2)
        try:
            # Assumes that graphviz already generated the svg
            ink_args = ["inkscape", "-D", "-z", "--file={}".format(filename1),
                        "--export-pdf={}".format(filename2)]
            subprocess.check_call(ink_args, startupinfo=STARTUPINFO)
        except OSError as e:
            if e.errno == errno.ENOENT:
                if force_ink:
                    raise
                return run_dot(dot, "pdf", prog, extra)
        with open(filename2, "rb") as file:
            return file.read()
    finally:
        os.remove(filename1)
        os.remove(filename2)


class DotDisplay(object):
    """Display class for Dot text"""

    def __init__(self, dot, format="png", prog="dot", extra=None):
        self.extensions = format
        if isinstance(format, str):
            self.extensions = [format]
        self.dot = dot
        self.prog = prog
        self.extra = extra

    def save(self, *files, formats=None):
        """Save dot file into specific format"""
        extensions = self.extensions
        formats = formats or [x.split('.')[-1] for x in files]
        self.extensions = set(formats)
        result = self.display_result()
        self.extensions = extensions
        for filename, format in zip(files, formats):
            mime = MIME_MAP.get(format.lower())
            if not mime:
                print("Invalid format {} for {}".format(format, filename))
                continue
            mode = "w"
            if mime in {"image/png", "application/pdf"}:
                mode = "wb"
            with open(filename, mode) as file:
                file.write(result[mime])

    def display_result(self):
        """Create display dictionary"""
        dot, prog, extra = self.dot, self.prog, self.extra
        result = OrderedDict()
        try:
            for ext in self.extensions:
                ext = ext.lower()
                mime = MIME_MAP.get(ext)
                if mime == "image/png":
                    result[mime] = run_dot(dot, "png", prog, extra)
                if mime == "image/svg+xml":
                    svg_text = run_dot(dot, "svg", prog, extra)
                    if svg_text is not None:
                        result[mime] = svg_text.decode("utf-8")
                if mime == "application/pdf":
                    if ext != "dot.pdf":
                        force_ink = ext == "ink.pdf"
                        result[mime] = dot_to_pdf(dot, prog, extra, force_ink)
                    else:
                        result[mime] = run_dot(dot, "pdf", prog, extra)
                if mime == "text/plain":
                    result[mime] = dot
                if mime == "text/vnd.graphviz":
                    result[mime] = dot

        except (OSError, IOError, RuntimeError) as err:
            sys.stderr.write("{}\n".format(err))
        if not result:
            sys.stderr.write("Fallback to dot text\n")
            result["text/plain"] = dot
        return result

    def _ipython_display_(self):
        result = self.display_result()
        display(result, raw=True)


@magics_class
class ProvMagic(Magics):
    @magic_arguments()
    @argument('-p', '--prog', default="dot", type=str, help="Command for rendering (dot, neato, ...)")
    @argument('-o', '--output', default="", type=str, help="Output base name")
    @argument('-e', '--extensions', default=["png"], nargs="+", help="List of extensions for produced files (e.g., provn, dot, png, svg, pdf, dot.pdf)")
    @argument('-x', '--width', default=16, type=int, help="Graph width")
    @argument('-y', '--height', default=12, type=int, help="Graph height")
    @argument('-r', '--rankdir', default="BT", type=str, help="Graph rankdir")
    @argument('-s', '--style', default="default", type=str, help="Graph style")
    @argument('extra', default=[], nargs='*', help="Extra options for graphviz")
    @cell_magic
    def provn(self, line, cell):
        # Remove comment on %%provn line
        pos = line.find("#")
        line = line[:pos if pos != -1 else None]

        formatter = DollarFormatter()
        line = formatter.vformat(
            line, args=[], kwargs=self.shell.user_ns.copy()
        )
        args = parse_argstring(self.provn, line)

        provn, dot_content = configure_graph(graph, args, cell)

        extensions = [x.lower() for x in args.extensions]

        if "provn" in extensions:
            if args.output:
                with open(args.output + ".provn", "w") as f:
                    f.write(provn)
            extensions.remove("provn")

        if not extensions:
            return "provn file created"

        dot_display = DotDisplay(dot_content, extensions, args.prog, args.extra)

        if args.output:
            dot_display.save(*((args.output + "." + ext) for ext in extensions))

        return dot_display

    @magic_arguments()
    @argument('-p', '--prog', default="dot", type=str, help="Command for rendering (dot, neato, ...)")
    @argument('-e', '--extensions', default=["png"], nargs="+", help="List of extensions for produced files (e.g., provn, dot, png, svg, pdf, dot.pdf)")
    @argument('-o', '--output', default="temp", type=str, help="Output base name")
    @argument('extra', default=[], nargs='*', help="Extra options for graphviz")
    @cell_magic
    def dot(self, line, cell):
        # pylint: disable=E0602
        # Remove comment on %%provn line
        pos = line.find("#")
        line = line[:pos if pos != -1 else None]

        formatter = DollarFormatter()
        line = formatter.vformat(
            line, args=[], kwargs=self.shell.user_ns.copy()
        )
        args = parse_argstring(self.dot, line)

        dot_display = DotDisplay(cell, args.extensions, args.prog, args.extra)
        if args.output:
            dot_display.save(*((args.output + "." + ext) for ext in args.extensions))

        return dot_display

def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    global LOADED   # pylint: disable=global-statement, invalid-name
    if not LOADED:
        ipython.register_magics(ProvMagic)
        LOADED = True
