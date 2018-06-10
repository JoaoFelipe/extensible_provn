from .provtoolbox import ProvToolboxStyle


class NoHighlightStyle(ProvToolboxStyle):

    def __init__(self):
        super(NoHighlightStyle, self).__init__()
        self.use_parsetime = False
        self.hide_namespace = False
        self.qualified_attr = True
        self.labelsize = "14"
        self.join(self.style, {
            #"hadMember_label": lambda l, a: self.taillabel("[ ]", a),
            "derivedByInsertionFrom1": {"arrowhead": "none"},
            "derivedByInsertionFrom_label*": self.label,
            "hadDictionaryMember_label*": self.label,

            "value": {"fillcolor": "#FFFC87", "color": "#808080", "style": "filled"},
            "accessed_label*": self.label,
            "accessedPart_label*": self.label,
            "defined_label*": self.label,
            "wasDefinedBy_label*": self.label,
            "derivedByInsertion1": {"style":"dashed"},
            "derivedByInsertion_label*": self.label,
            "derivedByRemoval_label*": self.label,

            "version": {"fillcolor": "#FFFC87", "color": "#808080", "style": "filled"},
            "int_wasDerivedFrom1": {"arrowhead": "none"},
            "int_wasDerivedFrom0": {"style":"dashed"},
            "int_wasDerivedFrom_label*": self.label,
            "int_used_label*": self.label,
            "int_wasGeneratedBy_label*": self.label,

            "ver_wasDerivedFrom1": {"arrowhead": "none"},
            "ver_wasDerivedFrom0": {"style":"dashed"},
            "ver_hadMember_label*": self.label,
            "ver_wasDerivedFrom_label*": self.label,
            "ver_used_label*": self.label,
            "ver_wasGeneratedBy_label*": self.label,
        })

    def label(self, label, attrs):
        if label:
            return {
                "fontsize": self.labelsize,
                "distance": "1.5",
                "angle": "60.0",
                "rotation": "20",
                "label": label.replace('"', '\\"')
            }
        return {}


EXPORT = NoHighlightStyle
