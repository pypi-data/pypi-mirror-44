"""
Extensions of iterable data types, enabling bounds wise bookmarking indexing and active item setting
Enables iterable passing while preserving bookmarks
"""
from collections import OrderedDict


def Itermark(iterable):
    """
    Extensions for iterable data types, enabling boudwise bookmarking and
    active item tracking/ and setting (type allowing)
    Whole itermark obj can be passed, preserving bookmark

    - mark: Bookmark index of underlying iterable. Supports direct and operator assignment
    - active: Active item, based off current mark index. Allows read/write usage (type allowing)

    Args:
        iterable: Iterable object type, to add Itermark functionality to

    Returns:
        Itermark object, matching the given iterable type
    """

    if isinstance(iterable, list):
        from ._list import ItermarkList
        return ItermarkList(iterable)

    elif type(iterable) == type(OrderedDict()):     # Type compares used to avoid issues with
        from ._ordict import ItermarkOrDict         # Liskov Substitution Principle re dict types
        return ItermarkOrDict(iterable)             # isinstance(OrderedDict(), dict) == True
    # See commented out rough draft classful solution below, for possibly scalable solution
    elif type(iterable) == type({}):    # standard dict
        from ._dict import ItermarkDict
        return ItermarkDict(iterable)

    elif isinstance(iterable, set):
        from ._set import ItermarkSet
        return ItermarkSet(iterable)

    elif isinstance(iterable, str):
        from ._str import ItermarkStr
        return ItermarkStr(iterable)

    elif isinstance(iterable, tuple):
        from ._tuple import     ItermarkTuple
        return ItermarkTuple

    else:
        raise TypeError(f"Currently unsupported type! \n {type(iterable)}")



# from typing import Dict
# class _Itermark:

    # def __init__(self, iterable):
        # ...


    # def __new__(self, iterable):
        # self.itermark_maker: Dict[type, property] = {
            # type([]):               self.return_itermark_list,
            # type({}):               self.return_itermark_dict,
            # type(set()):            'set',
            # type(''):               'string',
            # type(()):               'tuple',
            # type(OrderedDict()):    'od',
        # }
        # # type handler dict adds overhead, but removes issues with Liskov Substitution Principle,
        # # (where child classes are substitutable for their parents)

        # try:
            # self.iterable = iterable
            # print(type(self.iterable))
            # print(type(list))
            # print(type(self.iterable) == type(list))
            # input()
            # return self.itermark_maker[type(self.iterable)]
        # except KeyError:
            # raise TypeError(f"Currently unsupported type! \n {type(iterable)}")

    # @property
    # def return_itermark_list(self):
        # from ._list import ItermarkList
        # print('imported list')
        # return ItermarkList(self.iterable)

    # @property
    # def return_itermark_dict(self):
        # from ._dict import ItermarkDict
        # print('imported dict')
        # return ItermarkDict(self.iterable)

    # @property
    # def return_itermark_ordict(self):
        # from ._ordict import ItermarkOrDict
        # return ItermarkOrDict(self.iterable)

    # @property
    # def return_itermark_set(self):
        # from ._set import ItermarkSet
        # return ItermarkSet(self.iterable)

    # @property
    # def return_itermark_str(self):
        # from ._str import ItermarkStr
        # return ItermarkStr(self.iterable)

    # @property
    # def return_itermark_tup(self):
        # from ._tuple import ItermarkTuple
        # return ItermarkTuple
