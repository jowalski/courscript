from courscript.folder import CourseFilelist
from courscript.header import CourseHeaderList
from courscript.sub import CourseSublist
from courscript.para import CourseParalist
import sys


class Courscript:

    def __init__(self, title_dir, path="*/*.srt", base=1):
        self.title_dir = title_dir
        self.srt_path = path
        self.filelist = CourseFilelist(self.title_dir, self.srt_path)
        self.headerlist = CourseHeaderList(self.filelist, base)

    def print(self, file=sys.stdout, base=1):
        """Print a md file of subtitle transcripts.
        """
        for headers, srt_file in zip(self.headerlist, self.filelist):
            srtlst = CourseSublist(srt_file.path)
            paras = CourseParalist(srtlst, headers)
            paras.print(file)
