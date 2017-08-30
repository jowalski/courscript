import pysrt
import itertools

from collections import UserList
from pysrt.srtitem import SubRipItem


class Sub(SubRipItem):

    def __init__(self, subitem=None):
        if subitem is None:
            SubRipItem.__init__(self)
        else:
            SubRipItem.__init__(self, subitem.index, subitem.start,
                                subitem.end, subitem.text, subitem.position)

    # def __repr__(self):
    #     # values = [reprlib.repr(self.text),
    #     #           format_start_end(self.start, self.end),
    #     #           'break' if self.isbreak else 'cont']
    #     values = [reprlib.repr(self.ftext),
    #               format_start_end(self.fstart, self.fend)]
    #     value_str = ', '.join('{}'.format(i) for i in values)
    #     return '{}({})'.format(self.__class__.__name__, value_str)

    @property
    def ftext(self):
        return self.text.encode('utf-8')

    @property
    def fstart(self):
        return self.start.to_time()

    @property
    def fend(self):
        return self.end.to_time()

    def is_break(self, other):
        return other is None or self.end < other.start

    # def is_break_of_at_least_t(self, other, t):
    #     return self.end < other.start - t


class SubFile:
    """
    SubFile(filename)

    Iterable, of \"SubGroup\"s.

    subgroups = list(SubFile(filename))
    """

    def __init__(self, filename):
        self.filename = filename
        self.subiter = self._open(filename)

    def __iter__(self):
        return self.group_subs(self.subiter)

    @classmethod
    def group_subs(cls, subtitle_iter):
        subgroup = Subgroup()
        for sub1, sub2 in cls.pairwise(subtitle_iter):
            subgroup.append(sub1)
            if sub1.is_break(sub2):
                yield subgroup
                subgroup = Subgroup()

    def _file_wrapper(self, filename):
        # a missing file returns a blank Sublist rather than an error
        try:
            srts = pysrt.open(filename)
        except FileNotFoundError:
            srts = [Sub(None)]
        return srts

    def _open(self, filename):
        # return (Sub(sub) for sub in pysrt.open(filename))
        return (Sub(sub) for sub in self._file_wrapper(filename))

    @staticmethod
    def pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ...
        (from python documentation)
        """
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)


class Subgroup(UserList):
    """
    Subgroup(subtitles, start, end)

    subtitles: \"Sub\"s, consecutive in time
    start:     start time object, start of first Sub
    end:       end time object, end of last Sub

    Each subgroup is a set of subtitles, consecutive in time without breaks.
    """

    def __init__(self, subs=None, start=None, end=None):
        UserList.__init__(self, subs or [])
        self.start = start
        self.end = end

    def append(self, sub):
        """
        append(subtitle)

        Append a subtitle to the list. Update start and/or end time.
        """
        UserList.append(self, sub.text)
        if self.start is None:
            self.start = sub.fstart
        self.end = sub.fend
