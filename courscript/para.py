import textwrap
from courscript.timefuns import format_start_end
import reprlib
import sys


class CoursePara:

    wrapper = textwrap.TextWrapper()
    TIME_FMT = '%H:%M:%S'

    def __init__(self, sublist):
        self.text = self._join_text(sublist)
        self.start, self.end = sublist[0].start, sublist[-1].end

    def __repr__(self):
        start_end_str = format_start_end(self.start, self.end)
        values = [start_end_str, reprlib.repr(self.text)]
        value_str = ', '.join('{}'.format(i) for i in values)
        return '{}({})'.format(self.__class__.__name__, value_str)

    def __str__(self):
        return u'\n'.join(self.text)

    def start_end_md(self):
        return u'_({0} - {1})_'.format(self.start.strftime(self.TIME_FMT),
                                       self.end.strftime(self.TIME_FMT))

    def linecount(self):
        return len(self.text)

    def _join_text(self, sublist):
        text = u' '.join(subt.text.decode('utf-8') for subt in sublist)
        # use the text wrapper here to create nicely formatted lines
        return(self.wrapper.wrap(text))


class CourseParalist:

    def __init__(self, sublist, headers, print_times=False):
        self.paras = self._make_paras(sublist)
        self.headers = headers
        self.print_times = print_times

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
        return [CoursePara(sublist[slc]) for slc in sublist.slicebreaks()]
