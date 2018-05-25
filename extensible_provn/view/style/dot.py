from .default import DefaultStyle
from .nohighlight import NoHighlightStyle

class DotMixin:

    def __init__(self, *args, **kwargs):
        super(DotMixin, self).__init__(*args, **kwargs)
        self.dotignore = {'dot:htmlcolor', 'dot:hide', 'dot:specific', 'dot:hide2'}
        self.style = self.join(self.style, {
            "after": self.dotchange,
        })

    def dotchange(self, statement, args, current, attrs):
        result = {}
        for key, value in attrs.items():
            if key.startswith("dot:") and key not in self.dotignore:
                result[key[4:]] = value
        return result

    def htmlcolor(self, element, attrs):
        if 'dot:htmlcolor' in attrs:
            return '<font color={}>{}</font>'.format(attrs['dot:htmlcolor'], element)
        return element

class DotDefault(DotMixin, DefaultStyle):
    pass

class DotNoHighlight(DotMixin, NoHighlightStyle):
    pass

EXPORT = DotDefault
