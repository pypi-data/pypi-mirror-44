from collections import OrderedDict
from ._dict import ItermarkDict


class ItermarkOrDict(OrderedDict, ItermarkDict):
    """Itermark Ordered Dict object, extending default dict functionality"""
    # Inherits ItermarkDict properties
