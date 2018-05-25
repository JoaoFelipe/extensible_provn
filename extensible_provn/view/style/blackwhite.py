from .nohighlight import NoHighlightStyle

class BlackWhiteStyle(NoHighlightStyle):

    def __init__(self):
        super(BlackWhiteStyle, self).__init__()
        self.style = self.join(self.style, {
            "entity": {"fillcolor": "#FFFFFF", "color": "#000000", "style": "filled"},
            "activity": {
                "fillcolor": "#FFFFFF", "color": "#000000",
                "shape": "polygon", "sides": "4", "style": "filled"
            },
            "agent": {"fillcolor": "#FFFFFF", "color": "#000000", "shape": "house", "style": "filled"},
            "value": {"fillcolor": "#FFFFFF", "color": "#000000", "style": "filled"},
            "version": {"fillcolor": "#FFFFFF", "color": "#000000", "style": "filled"},
        })


EXPORT = BlackWhiteStyle
