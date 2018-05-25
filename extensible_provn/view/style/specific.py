from .hide import DotHide

class DotSpecific(DotHide):

    def __init__(self, specific1="#00ff99", specific2="#006600", **kwargs):
        super(DotSpecific, self).__init__(**kwargs)
        self.specific1 = specific1
        self.specific2 = specific2

    def dotchange(self, statement, args, current, attrs):
        result = super(DotSpecific, self).dotchange(statement, args, current, attrs)
        if "dot:specific" in attrs:
            if "fillcolor" in current:
                result["fillcolor"] = self.specific1
            result["fontcolor"] = self.specific2
            result["color"] = self.specific2
        return result


EXPORT = DotSpecific