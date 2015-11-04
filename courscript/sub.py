import pysrt
import itertools
import reprlib
from courscript.timefuns import format_start_end
from courscript.error import CoursError


class CourseSub:

    def __init__(self, subripitem):
        self.text = subripitem.text.encode('utf-8')
        self.start = subripitem.start.to_time()
        self.end = subripitem.end.to_time()
        self.isbreak = False

    def __repr__(self):
        values = [reprlib.repr(self.text),
                  format_start_end(self.start, self.end),
                  'break' if self.isbreak else 'cont']
        value_str = ', '.join('{}'.format(i) for i in values)
        return '{}({})'.format(self.__class__.__name__, value_str)

    def __lt__(self, other):
        return self.end < other.start

    def __gt__(self, other):
        return self.start > other.end

    def __sub__(self, other):
        """Subs must be separate for this (and lt, eq) to be meaningful.
        """
        if self < other:
            return other.start - self.end
        elif self > other:
            return self.start - other.end
        else:
            raise CoursError('Subtracting non-separate CourseSubs')

    def set_break(self):
        self.isbreak = True


class CourseSublist:

    def __init__(self, filename):
        sublist = self.open(filename)
        self.sublist = self._mark_breaks(sublist)

    def __repr__(self):
        values = ', '.join('{!r}'.format(i) for i in self.sublist)
        return '{}({})'.format(self.__class__.__name__, values)

    def __getitem__(self, position):
        return self.sublist[position]

    def open(self, filename):
        sublist = [CourseSub(sub) for sub in pysrt.open(filename)]
        return(sublist)

    def _mark_breaks(self, subs):
        for sub1, sub2 in self.pairwise(subs):
            # mark 'break' if second subtitle doesn't begin
            # where the first ends
            if sub1 < sub2:
                sub1.set_break()
        return(subs)

    def slicebreaks(self):
        """slice by breaks
        """
        breaks = [i + 1 for i, subt in enumerate(self.sublist) if subt.isbreak]
        starts, breaks = [0] + breaks, breaks + [len(self.sublist)]
        return (slice(a, b) for a, b in zip(starts, breaks))

    @staticmethod
    def pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ...
        (from python documentation)
        """
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)
