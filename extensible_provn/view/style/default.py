from .nohighlight import NoHighlightStyle

class DefaultStyle(NoHighlightStyle):

    def __init__(self, highlight="darkgreen", highlight_node="#32CD32"):
        super(DefaultStyle, self).__init__()
        self.highlight = highlight
        self.style = self.join(self.style, {
            "value": {"fillcolor": highlight_node, "color": "#808080", "style": "filled"},
            "version": {"fillcolor": highlight_node, "color": "#808080", "style": "filled"},
        })

    def label(self, label, attrs):
        if label:
            return {
                "fontsize": self.labelsize,
                "labeldistance": "1.5",
                "color": self.highlight,
                "labelangle": "60.0",
                "rotation": "20",
                "label": label.replace('"', '\\"')
            }
        return {"color": self.highlight}

EXPORT = DefaultStyle
