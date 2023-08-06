"""
Base engine for itermark functionality.

Extension for iterable data types; adds boundwise bookmark iteration, enabling active item
tracking/setting (type allowing)
"""

from typing import Optional


class ItermarkEngine:
    """
    Base engine, inhereted by type specific implementations

    - mark: Bookmark index of underlying iterable. Supports direct and operator assignment
    - active: Active item, based off current mark index. Read/write usage, type allowing
    """

    _mark = None
    """Protected bookmark index; access via property mark so boundary checks are run"""

    @property
    def mark(self) -> Optional[int]:
        """
        Get current active bookmark index

        Returns:
                Active bookmark index, or None if len=0
        """
        if self._is_loaded:
            return self._mark
        return None

    @mark.setter
    def mark(self, new_mark: int):
        """
        Attempts to set active mark. Raises IndexError if new_mark is out of bounds

        Arguments:
            new_mark:
                Desired new bookmark index
        """

        if self._is_loaded:
            if not isinstance(new_mark, int):
                raise TypeError(f"marklist index must be integer, not {str(type(new_mark))}")

            # No negatives. -= 1 fouls up indexing when _mark is 0
            if new_mark < 0:
                self._mark = 0
            # Max length check
            elif self._mark_is_over_bounds(new_mark):
                self.markend()
            else:
                self._mark = new_mark

    @property
    def active(self) -> any:
        """
        Get current active item, based off bookmark index

        Returns:
                Active item, or None if len=0
        """
        if self._is_loaded:
            return self[self._mark]
        return None

    @active.setter
    def active(self, val: any):
        """
        Set active list item, based on current mark value

        Args:
            val: new value for current active item
        """
        if self._is_loaded:
            self[self._mark] = val

    def markend(self):
        """
        Set mark to end value. Mark will never go above upper bound, but without calling len() user may not
        know what that upper bound is. Use .markend() to reliably set mark to upper bound
        """
        if self._is_loaded:
            self.mark = self.__len__()

    # ItermarkEngine maintenance

    @property
    def _is_loaded(self) -> bool:
        """Property to shutdown itermark functions if iterable is empty"""
        if self.__len__() == 0:
            self._deactivate_mark()
            return False
        self._activate_mark()
        return True

    def _deactivate_mark(self):
        """Used to disable callable attributes, if iterable becomes empty"""
        self._mark = None
        # .active is never stored, instead called from _mark

    def _activate_mark(self):
        """Ensures _ndx is activated and within bounds. Iterable is assumed non-empty"""
        if not self._mark or self._mark < 0:
            self._mark = 0
        if self._mark_is_over_bounds():
            self.markend()

    def _mark_is_over_bounds(self, mark_check=None):
        """
        Funnel function, verify if mark_check is within bounds of upper length. Default self._mark
        Typically followed by self.markend()

        Args:
            mark_check: Mark to check. Defaults to self._mark, but can be passed an externally given
            mark instead
        Returns:
            Bool, indicating if mark is >= self.__len__
        """
        if not mark_check:
            mark_check = self._mark
        return mark_check >= self.__len__()

    # Hollow references, to be overwritten by each subtypes' specific version.
    # ItermarkEngine functions will then reference the actual function

    def __len__(self):
        """Hollow reference. Itermarks use default types first, so this will not overwrite"""

    def __iter__(self):
        """Hollow reference. Itermarks use default types first, so this will not overwrite"""

    def __getitem__(self):
        """Hollow reference. Itermarks use default types first, so this will not overwrite"""

    def __setitem__(self):
        """Hollow reference. Itermarks use default types first, so this will not overwrite"""
