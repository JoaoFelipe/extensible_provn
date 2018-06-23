from .specific import DotSpecific
from functools import partial
import re

class DotPaper(DotSpecific):

    def __init__(self, **kwargs):
        super(DotPaper, self).__init__(**kwargs)
        self.labelsize = "36"
        self.node_labelsize = "36"
        self.tail_labelsize = "30"
        self.attrs_labelsize = "24"
        self.use_parsetime = True
        self.hide_namespace = True

        self.specific2 = "#800000"
        self.specific1 = "#ffe6e6"
        self.style = self.join(self.style, {
            "ver_wasDerivedFrom0": {"style":"dashed", "color": self.specific2},
            "ver_wasDerivedFrom2_label*": self.custom_label,
            "hadMember_label": lambda l, a: self.taillabel("", a),
        })

    def after_node(self, statement, args, current, attrs):
        label, url = args
        return {
            "label": label.replace('"', '\\"'),
            "URL": url,
            "fontsize": self.node_labelsize,
        }

    def custom_label(self, label, attrs):
        res = self.join(self.label(label, attrs, color=self.specific2), {
            "color": "black",
            "fontcolor": self.specific2,
        })
        return res


    def taillabel(self, label, attrs):
        if "dot:specific" in attrs:
            return self.label(label, attrs, color=self.specific1)
        if label:
            return {
                "labelfontsize": self.tail_labelsize,
                "labeldistance": "5",
                "labelangle": "60.0",
                "rotation": "20",
                "taillabel": label.replace('"', '\\"')
            }
        return {}

    def label(self, label, attrs, color="black"):
        if label:
            if color == "black" and not "dot:hide2" in attrs and not "dot:specific" in attrs:

                split = re.split(r'( |\n)', label)
                part1 = '<font color="{}">{}</font>'.format(color, split[0])
                part2 = ""
                if len(split) > 1:
                    part2 = "".join(split[1:]).replace("\n", "<br/>").replace(" ", "&nbsp;")
                    part2 = '<font color="{}">{}</font>'.format(self.specific2, part2)
                label = ("<{}{}>".format(part1, part2))
            else:
                label = label.replace('"', '\\"')
            return {
                "fontsize": self.labelsize,
                "labeldistance": "3",
                "color": color,
                "labelangle": "60.0",
                "rotation": "20",
                "label": label
            }
        return {"color": color}


EXPORT = DotPaper