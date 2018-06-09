from collections import OrderedDict
from functools import partial
from ...utils import parsetime

class ProvToolboxStyle(object):

    def __init__(self):
        self.qualified_attr = False
        self.tail_labelsize = "8"
        self.attrs_labelsize = "10"
        self.style = {
            "node_after": self.after_node,
            "label": self.taillabel,
            "point": {"shape": "point", "label": ""},
            "attrs": self.attrs_node,
            "attrs_arrow": {
                "color": "gray",
                "style": "dashed",
                "arrowhead": "none",
            },

            "entity": {"fillcolor": "#FFFC87", "color": "#808080", "style": "filled"},
            "activity": {
                "fillcolor": "#9FB1FC", "color": "#0000FF",
                "shape": "polygon", "sides": "4", "style": "filled"
            },
            "agent": {"fillcolor": "#FDB266", "shape": "house", "style": "filled"},

            "wasStartedBy1": {"arrowhead": "none", "dir": "back", "arrowtail": "oinv"},
            "wasStartedBy3": {"dir": "back", "arrowtail": "oinv"},
            "wasEndedBy1": {"arrowhead": "none", "dir": "back", "arrowtail": "odiamond"},
            "wasEndedBy3": {"dir": "back", "arrowtail": "odiamond"},
            "wasInvalidatedBy": {"dir": "both", "arrowtail": "odiamond"},
            "wasAssociatedWith1": {"arrowhead": "none"},
            "actedOnBehalfOf1": {"arrowhead": "none"},
        }

    def after_node(self, statement, args, current, attrs):
        label, url = args
        return {
            "label": label.replace('"', '\\"'),
            "URL": url,
        }

    def taillabel(self, label, attrs):
        if label:
            return {
                "labelfontsize": self.tail_labelsize,
                "labeldistance": "1.5",
                "labelangle": "60.0",
                "rotation": "20",
                "taillabel": label.replace('"', '\\"')
            }
        return {}

    def attrs_node(self, label, attrs):
        return {
            "color": "gray",
            "shape": "note",
            "fontsize": self.attrs_labelsize,
            "fontcolor": "black",
            "label": label,
        }

    def arrow(self, attrs, statement, label="", extra=""):
        label_dict = {}
        self.apply(label_dict, "label", label, attrs)
        self.apply(label_dict, statement + "_label", label, attrs)
        if extra:
            self.apply(label_dict, statement + extra + "_label", label, attrs)

        arrow_dict = {}
        self.apply(arrow_dict, "arrow", attrs)
        self.apply(arrow_dict, statement, attrs)
        if extra:
            self.apply(arrow_dict, statement + extra, attrs)

        result = self.join(label_dict, arrow_dict)
        self.apply(result, "after", statement, (extra,), result, attrs)
        self.apply(result, "arrow_after", statement, (extra,), result, attrs)
        return result

    def point(self, attrs, statement, extra=""):
        result = {}
        self.apply(result, "point", attrs)
        self.apply(result, statement + "_point", attrs)
        if extra:
            self.apply(result, statement + extra + "_point", attrs)

        self.apply(result, "after", statement, (extra,), result, attrs)
        self.apply(result, "point_after", statement, (extra,), result, attrs)
        return result

    def node(self, attrs, statement, label="", url=""):
        result = {}
        self.apply(result, "node", label, url, attrs)
        self.apply(result, statement, label, url, attrs)

        self.apply(result, "after", statement, (label, url), result, attrs)
        self.apply(result, "node_after", statement, (label, url), result, attrs)
        return result

    def attrs(self, attrs, statement, label=""):
        result = {}
        self.apply(result, "attrs", label, attrs)
        self.apply(result, statement + "_attrs", label, attrs)

        self.apply(result, "after", statement, (label,), result, attrs)
        self.apply(result, "attrs_after", statement, (label,), result, attrs)
        return result

    def attrs_arrow(self, attrs, statement):
        result = {}
        self.apply(result, "attrs_arrow", attrs)
        self.apply(result, statement + "_attrs_arrow", attrs)

        self.apply(result, "after", statement, tuple(), result, attrs)
        self.apply(result, "attrs_arrow_after", statement, tuple(), result, attrs)
        return result

    def apply(self, result, name, *args):
        access = OrderedDict()
        if name in self.style:
            access = self.style[name]
        if name + "*" in self.style:
            access = self.style[name + "*"]
            result.clear()
        if callable(access):
            access = access(*args)
        for key, value in access.items():
            result[key] = value
        return result

    def filter_attr(self, key, value, attrs):
        return not key.startswith("dot:")

    def htmlcolor(self, element, attrs):
        return element

    def change_attr(self, key, value):
        key = key.split(":", maxsplit=1)[-1]
        tvalue = parsetime(value)
        if tvalue:
            value = str(tvalue)
        else:
            value = value.split(":", maxsplit=1)[-1]
        return key, value

    def join(self, new, *dicts):
        for dic in dicts:
            for key, value in dic.items():
                new[key] = value
        return new

EXPORT = ProvToolboxStyle
