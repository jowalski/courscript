import textwrap
from courscript.timefuns import format_start_end
import reprlib
import sys
import datetime


class Para:

    wrapper = textwrap.TextWrapper()
    TIME_FMT = '%H:%M:%S'

    def __init__(self, text, start=None, end=None):
        self.text = text
        self.start = datetime.time(0) if start is None else start
        self.end = datetime.time(0) if end is None else end

    @classmethod
    def subs(cls, sublist):
        text = u' '.join(subt.text.decode('utf-8') for subt in sublist)
        wtext = u'\n'.join(cls.wrapper.wrap(text))
        start, end = sublist[0].start, sublist[-1].end
        # use the text wrapper here to create nicely formatted lines
        return cls(wtext, start, end)

    @classmethod
    def slide(cls, slide):
        text = u'![{alt}]({path})'.format(alt=slide, path=slide.path)
        return cls(text)

    def __repr__(self):
        start_end_str = format_start_end(self.start, self.end)
        values = [start_end_str, reprlib.repr(self.text)]
        value_str = ', '.join('{}'.format(i) for i in values)
        return '{}({})'.format(self.__class__.__name__, value_str)

    def __str__(self):
        return self.text

    def start_end_md(self):
        return u'_({0} - {1})_'.format(self.start.strftime(self.TIME_FMT),
                                       self.end.strftime(self.TIME_FMT))

    def linecount(self):
        return len(self.text)


class Paralist:

    def __init__(self, sublist, headers, slidelist=None, print_times=False):
        self.paras = self._make_paras(sublist)
        self.headers = headers
        self.print_times = print_times
        self.slidelist = slidelist
        if slidelist is not None:
            self._add_slides()

    def __repr__(self):
        values = ', '.join('{!r}'.format(i) for i in self.paras)
        return '{}({})'.format(self.__class__.__name__, values)

    def __getitem__(self, position):
        return self.paras[position]

    def _print2nl(self, obj):
        print(obj, end='\n\n', file=self._fileio)

    def print(self, file=sys.stdout):
        self._fileio = file
        for hdr in self.headers:
            self._print2nl(hdr)
        for para in self.paras:
            if self.print_times:
                self._print2nl(para.start_end_md())
            self._print2nl(para)

    def _make_paras(self, sublist):
        """Form paragraphs from a list of subtitles.
        """
        return [Para.subs(sublist[slc]) for slc in sublist.slicebreaks()]

    def _add_slides(self):
        ls, lp = len(self.slidelist), len(self.paras)
        if lp < ls:
            insertpos = list(range(lp)) + ([lp - 1] * (ls - lp))
        else:
            insertpos = [round(i * lp / ls) for i in range(ls)]
        for i, slide in zip(reversed(insertpos), reversed(self.slidelist)):
            self.paras.insert(i + 1, Para.slide(slide))
