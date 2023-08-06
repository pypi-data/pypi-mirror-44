class ButtonsDict(dict):
    """A simple dict that allows indexing and inserting.

    For the obvious price of performance on insertions.
    """

    __slots__ = ('__index__', '_internal', )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__index__ = []

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, *args):
        if isinstance(args[0], tuple):
            super().__setitem__(args[0][1], args[1])
            self.__index__.insert(args[0][0], (args[0][1]))
        else:
            super().__setitem__(args[0], args[1])
            self.__index__.append(args[0])

    def __delitem__(self, key):
        super().__delitem__(key)
        self.__index__.remove(key)

    def __iter__(self):
        return iter(self.__index__)

    def __len__(self):
        return len(self.__index__)
