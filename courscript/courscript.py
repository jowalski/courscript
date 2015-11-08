from courscript.folder import CourseFilelist
from courscript.header import HeaderList
from courscript.sub import Sublist
from courscript.para import Paralist
from courscript.slide import CoursePdflist
import os.path
import sys


class Courscript:

    def __init__(self, title_dir, path="*/*.srt", base=1,
                 split=u'_', sub=u'-', pdfpath=False):
        self.title_dir = title_dir
        self.srt_path = path
        self.pdfpath = pdfpath
        self.filelist = CourseFilelist(title_dir, path, split, sub)
        self.headerlist = HeaderList(self.filelist, base)
        self.ispdf = False if not pdfpath else True
        self.pdflist = None if not pdfpath else \
            CoursePdflist(title_dir, pdfpath, split, sub)

    def print(self, file=sys.stdout, base=1):
        """Print a md file of subtitle transcripts.
        """
        if self.ispdf:
            self._print_wslides(file, base)
        for headers, srt_file in zip(self.headerlist, self.filelist):
            srtlst = Sublist(srt_file.path)
            paras = Paralist(srtlst, headers)
            paras.print(file)

    def _print_wslides(self, file=sys.stdout, base=1):
        print('Adding slides...')
        for headers, srt_file, pdf in \
                zip(self.headerlist, self.filelist, self.pdflist):
            srtlst = Sublist(srt_file.path)
            slidelist = pdf.slist
            paras = Paralist(srtlst, headers, slidelist)
            paras.print(file)
