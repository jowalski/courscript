import textwrap
from courscript.timefuns import format_start_end
import reprlib
import sys
from collections import UserString, UserList
from courscript.sub import SubFile


class Para(UserString):
    """
    Para(subtitle_group)

    Convert a subtitle group to a paragraph of wrapped text.
    """

    wrapper = textwrap.TextWrapper()
    TIME_FMT = '%H:%M:%S'

    def __init__(self, subtitle_group):
        # self.text = u'\n'.join(cls.wrapper.wrap(u' '.
        # join(subt.text for subt        # in sublist)))
        UserString.__init__(self, self._wrap(subtitle_group))
        self.start = subtitle_group.start
        self.end = subtitle_group.end

    def _wrap(self, subtitle_group):
        return self.wrapper.fill(u' '.join(subtitle_group.data))

    # def slide(cls, slide):
    #     text = u'![{alt}]({path})'.format(alt=slide, path=slide.path)
    #     return cls(text)

    def __repr__(self):
        start_end_str = format_start_end(self.start, self.end)
        values = [start_end_str, reprlib.repr(self.data)]
        value_str = ', '.join('{}'.format(i) for i in values)
        return '{}({})'.format(self.__class__.__name__, value_str)

    def __str__(self):
        return self.data

    def start_end_md(self):
        return u'_({0} - {1})_'.format(self.start.strftime(self.TIME_FMT),
                                       self.end.strftime(self.TIME_FMT))

    def linecount(self):
        return len(self.data)


class Paralist(UserList):

    def __init__(self, filename, slidelist=None,
                 print_times=False):
        UserList.__init__(self, self._make_paras(filename))
        self.print_times = print_times
        self.slidelist = slidelist or []
        if slidelist is not None:
            self._add_slides()

    def __repr__(self):
        values = ', '.join('{!r}'.format(i) for i in self.data)
        return '{}({})'.format(self.__class__.__name__, values)

    def _print2nl(self, obj):
        print(obj, end='\n\n', file=self._fileio)

    def print(self, file=sys.stdout):
        self._fileio = file
        for para in self.data:
            if self.print_times:
                self._print2nl(para.start_end_md())
            self._print2nl(para)

    @classmethod
    def _make_paras(cls, filename):
        """Make a list paragraphs from a subtitle file.
        """
        return [Para(sub_group) for sub_group in SubFile(filename)]

    # def _add_slides(self):
    #     ls, lp = len(self.slidelist), len(self.paras)
    #     if lp < ls:
    #         insertpos = list(range(lp)) + ([lp - 1] * (ls - lp))
    #     else:
    #         insertpos = [round(i * lp / ls) for i in range(ls)]
    #     for i, slide in zip(reversed(insertpos), reversed(self.slidelist)):
    #         self.paras.insert(i + 1, Para.slide(slide))
