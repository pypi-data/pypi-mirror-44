from ._z_itermark_engine import ItermarkEngine


# Note that this is designed around 3.6+'s insertion ordered dictionaries
# Recommend a Collections.OrderedDict for earlier implementations
class ItermarkDict(dict, ItermarkEngine):
    """ItermarkEngine dict object, extending default dict functionality"""

    @property
    def active(self) -> any:
        """
        Get current active val, based off bookmark index. For key, see ItermarkEngine.activekey

        Returns:
                Active key, or None if len=0
        """
        # Using an iterator object, return the nth item (where n = current _mark)
        if self._is_loaded:
            for ndx, key in enumerate(self.__iter__()):    # Iterates through keys
                if ndx == self._mark:
                    return self[key]

    @active.setter
    def active(self, val: any):
        """
        Set active dict value, based on currently marked key

        Args:
            val: new value for dict val
        """

        if self._is_loaded:
            for ndx, key in enumerate(self.__iter__()):
                if ndx == self._mark:
                    self[key] = val

    @property
    def activekey(self):
        """Get active key, rather than value"""
        if self._is_loaded:
            for ndx, key in enumerate(self.__iter__()):    # Iterates through keys
                if ndx == self._mark:
                    return key

    @activekey.setter
    def activekey(self, val):
        raise TypeError("ItermarkDict object does not support key assignment")

