

class Foo(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)