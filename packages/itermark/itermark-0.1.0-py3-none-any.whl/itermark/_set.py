from ._z_itermark_engine import ItermarkEngine


class ItermarkSet(set, ItermarkEngine):
    """ItermarkEngine set object, Adding bookmarking functionality"""
    # I don't know why this exists. Iterating through a set with a bookmark makes no sense

    @property
    def active(self) -> any:
        """
        Get current active item, based off bookmark index

        Returns:
                Active item, or None if len=0
        """
        # Using an iterator object, return the nth item (where n = current _mark)
        if self._is_loaded:
            for ndx, key in enumerate(self.__iter__()):  # Iterates through keys
                if ndx == self._mark:
                    return key

    @active.setter
    def active(self, val):
        raise TypeError("ItermarkSet object does not support item assignment")
