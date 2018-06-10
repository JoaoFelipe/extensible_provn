from .hide import DotHide


class DotPaper2(DotHide):

    def __init__(self, **kwargs):
        super(DotPaper2, self).__init__(**kwargs)
        self.use_parsetime = True
        self.hide_namespace = True


EXPORT = DotPaper2