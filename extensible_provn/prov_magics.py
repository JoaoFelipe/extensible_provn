import subprocess
import platform
import errno

from collections import deque

from IPython.display import display, Image, SVG
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.utils.text import DollarFormatter


from .view.dot import graph

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

def transform_dot(prog, dotfile, base, extensions):
    order = deque()
    output_ext = None
    for ext in reversed(extensions):
        if ext == "pdf":
            order.appendleft(("inkscape", "pdf"))
            order.append(("graphviz", "svg"))
            if output_ext is None:
                output_ext = "svg"
        elif ext == "dot.pdf":
            order.append(("graphviz", "pdf"))
        else:
            order.append(("graphviz", ext))
        if ext in ("png", "svg"):
            output_ext = ext

    while order:
        tool, dext = order.pop()
        dimage = base + "." + dext

        if tool == "graphviz":
            draw_args = [prog, dotfile, "-T{}".format(dext), "-o", dimage]
            subprocess.check_call(draw_args, startupinfo=STARTUPINFO)

        elif tool == "inkscape":
            try:
                # Assumes that graphviz already generated the svg
                svgimage = base + ".svg"
                ink_args = ["inkscape", "-D", "-z", "--file={}".format(svgimage),
                            "--export-pdf={}".format(dimage)]
                subprocess.check_call(ink_args, startupinfo=STARTUPINFO)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    order.append(("graphviz", "pdf"))

    return output_ext


@magics_class
class ProvMagic(Magics):
    @magic_arguments()
    @argument('-p', '--prog', default="dot", type=str, help="Command for rendering (dot, neato, ...)")
    @argument('-o', '--output', default="temp", type=str, help="Output base name")
    @argument('-e', '--extensions', default=["png"], nargs="+", help="List of extensions for produced files (e.g., provn, dot, png, svg, pdf, dot.pdf)")
    @argument('-x', '--width', default=16, type=int, help="Graph width")
    @argument('-y', '--height', default=12, type=int, help="Graph height")
    @argument('-r', '--rankdir', default="BT", type=str, help="Graph rankdir")
    @argument('-s', '--style', default="default", type=str, help="Graph style")
    @cell_magic
    def provn(self, line, cell):
        # Remove comment on %%provn line
        pos = line.find("#")
        line = line[:pos if pos != -1 else None]
        args = parse_argstring(self.provn, line)

        provn, dot_content = configure_graph(graph, args, cell)

        extensions = [x.lower() for x in args.extensions]

        if "provn" in extensions:
            with open(args.output + ".provn", "w") as f:
                f.write(provn)
            extensions.remove("provn")

        if not extensions:
            return "provn file created"


        dotfile = args.output + ".dot"
        with open(dotfile, "w") as f:
            f.write(dot_content)

        output_ext = transform_dot(args.prog, dotfile, args.output, extensions)

        if output_ext == "svg":
            return SVG(filename=args.output + ".svg")
        if output_ext == "png":
            return Image(args.output + ".png")

    @magic_arguments()
    @argument('-p', '--prog', default="dot", type=str, help="Command for rendering (dot, neato, ...)")
    @argument('-o', '--output', default="temp", type=str, help="Output base name")
    @argument('-e', '--extensions', default=["png"], nargs="+", help="List of extensions for produced files (e.g., provn, dot, png, svg, pdf, dot.pdf)")
    @cell_magic
    def dot(self, line, cell):
        # pylint: disable=E0602
        # Remove comment on %%provn line
        pos = line.find("#")
        line = line[:pos if pos != -1 else None]

        formatter = DollarFormatter()
        line = formatter.vformat(line, args=[],
                                 kwargs=get_ipython().user_ns.copy())
        args = parse_argstring(self.provn, line)

        extensions = [x.lower() for x in args.extensions]

        dotfile = args.output + ".dot"
        with open(dotfile, "w") as f:
            f.write(cell)

        output_ext = transform_dot(args.prog, dotfile, args.output, extensions)

        if output_ext == "svg":
            return SVG(filename=args.output + ".svg")
        if output_ext == "png":
            return Image(args.output + ".png")


def load_ipython_extension(ipython):
    ipython.register_magics(ProvMagic)
