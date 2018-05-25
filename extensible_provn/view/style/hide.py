from .dot import DotNoHighlight

class DotHide(DotNoHighlight):

    def __init__(self, hide1="#FAFAFA", hide2="#F0F0F0", hide3="#999999", **kwargs):
        super(DotHide, self).__init__(**kwargs)
        self.hide1 = hide1
        self.hide2 = hide2
        self.hide3 = hide3

    def dotchange(self, statement, args, current, attrs):
        result = super(DotHide, self).dotchange(statement, args, current, attrs)
        if "dot:hide" in attrs:
            if "fillcolor" in current:
                result["fillcolor"] = self.hide1
            result["fontcolor"] = self.hide2
            result["color"] = self.hide2
        if "dot:hide2" in attrs:
            if "fillcolor" in current:
                result["fillcolor"] = self.hide1
            result["fontcolor"] = self.hide3
            result["color"] = self.hide3
        return result

    def filter_attr(self, key, value, attrs):
        if "dot:hide" in attrs:
            return False
        if "dot:hide2" in attrs:
            if key == "dot:hide2":
                return False
            return attrs["dot:hide2"] == "~attr"
        return not key.startswith("dot:")

EXPORT = DotHide