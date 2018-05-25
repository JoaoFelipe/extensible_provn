from extensible_provn.view.style.nohighlight import NoHighlightStyle

class WhiteBlackStyle(NoHighlightStyle):

    def __init__(self):
        super(WhiteBlackStyle, self).__init__()
        self.style = self.join(self.style, {
            "entity": {"fillcolor": "#000000", "fontcolor": "#FFFFFF", "style": "filled"},
            "activity": {
                "fillcolor": "#000000", "fontcolor": "#FFFFFF",
                "shape": "polygon", "sides": "4", "style": "filled"
            },
            "agent": {"fillcolor": "#000000", "fontcolor": "#FFFFFF", "shape": "house", "style": "filled"},
            "value": {"fillcolor": "#000000", "fontcolor": "#FFFFFF", "style": "filled"},
            "version": {"fillcolor": "#000000", "fontcolor": "#FFFFFF", "style": "filled"},
        })


EXPORT = WhiteBlackStyle