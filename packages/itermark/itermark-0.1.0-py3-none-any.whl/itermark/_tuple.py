from ._z_itermark_engine import ItermarkEngine


class ItermarkTuple(tuple, ItermarkEngine):
    """ItermarkEngine Tuple object, Adding bookmarking functionality"""

    @property
    def active(self):
        """Call to super Engine's active property. Here for setter's reference"""
        return super(ItermarkEngine).active

    @active.setter
    def active(self, val):
        raise TypeError("ItermarkTuple object does not support item assignment")
