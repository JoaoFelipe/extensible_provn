from .default import DefaultStyle


class DotPaper3(DefaultStyle):

    def __init__(self, **kwargs):
        super(DotPaper3, self).__init__(**kwargs)
        self.use_parsetime = True
        self.hide_namespace = True


EXPORT = DotPaper3