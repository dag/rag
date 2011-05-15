class ReusableMixin(object):

    @classmethod
    def using(cls, **overrides):
        return type(cls.__name__, (cls,), overrides)
