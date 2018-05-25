from .hide import DotHide


class DotPaper2(DotHide):

    def __init__(self, **kwargs):
        super(DotPaper2, self).__init__(**kwargs)
        self.style = self.join(self.style, {
            "ver_wasDerivedFrom0": {"style":"dashed"},
        })


    def taillabel(self, label, attrs):
        if "dot:specific" in attrs:
            return self.label(label, attrs, color="black")
        return super().taillabel(label, attrs)

    def label(self, label, attrs, color="black"):
        if label:
            return {
                "labelfontsize": self.labelsize,
                "labeldistance": "1.5",
                "color": color,
                "labelangle": "60.0",
                "rotation": "20",
                "label": label.replace('"', '\\"')
            }
        return {"color": color}


EXPORT = DotPaper2