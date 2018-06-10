import dateutil.parser
import sys

from pkg_resources import resource_string, resource_listdir, resource_isdir

MODULE = __name__
MODULE = MODULE[:MODULE.rfind(".")]


try:
    from html import escape
    from importlib import reload as reload_module
except ImportError:
    # Python 2
    def escape(s, quote=True):
        """
        Replace special characters "&", "<" and ">" to HTML-safe sequences.
        If the optional flag quote is true (the default), the quotation mark
        characters, both double quote (") and single quote (') characters are also
        translated.

        Code from CPython 3.6
        """
        s = s.replace("&", "&amp;") # Must be done first!
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        if quote:
            s = s.replace('"', "&quot;")
            s = s.replace('\'', "&#x27;")
        return s

    from imp import reload as reload_module

def unquote(value):
    if value and value.startswith('"'):
        value = value[1:-1]
    return value

def parsetime(time):
    time = unquote(time)
    if time and time.startswith("T") and time[1:].isdigit():
        return int(time[1:])
    elif time and time.isdigit():
        return int(time)
    try:
        return dateutil.parser.parse(time) if time else None
    except ValueError:
        return None


def resource(filename, encoding=None):
    """Access resource content via setuptools"""
    content = resource_string(MODULE, filename)
    if encoding:
        return content.decode(encoding=encoding)
    return content

def version():
    return resource("resources/version.txt", encoding="utf-8").strip()
