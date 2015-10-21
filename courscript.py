import os
import glob
import re
import pysrt
import itertools
import textwrap
import collections


class Courscript:
    TEXT, START, END, LINE = 0, 1, 2, 3

    def __init__(self, title_dir, path="*/*.srt"):
        self.title_dir, self.srt_path = title_dir, path

<<<<<<< HEAD
    title_dir = ''
    srt_path = ''
=======
>>>>>>> d770ce59837f9c22a0f95409feb04b480a4158ee
    wrapper = textwrap.TextWrapper()

    @classmethod
    def parse_fdname(cls, dirname):
        """Split a file or directory name into component parts.

        This at least works for coursera, the ml-foundations course hierarchy.
        """
        num, name = re.split('_', dirname)
        try:
            title, ext = re.split('\.', name)
        except ValueError:
            return int(num), re.sub('-', ' ', name)
        return int(num), re.sub('-', ' ', title), ext

    @classmethod
    def parse_srt_path(cls, path):
        """Parse a path string into a tuple using os.path.split recursively.
        """
        head, tail = os.path.split(path)
        tail_lst = [cls.parse_fdname(tail)]
        if not head:
            return tail_lst
        return(cls.parse_srt_path(head) + tail_lst)

    @classmethod
    def get_filelist(cls, pattern):
        """Get a list of files from globbing a pattern, including parsed title info.

        Parsed info includes section, lecture number and title info.
        """
        filelist = [(cls.parse_srt_path(srt), srt)
                    for srt in glob.glob(pattern)]
        return filelist

    @staticmethod
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    @classmethod
    def srttolist(cls, file):
        """Convert srt subtitle file to list of subtitle elements.

        Each element consists of [text, start, end, 'continue'/'break'] fields.
        """
        # pysrt does try to open in the proper encoding
        subs = pysrt.open(file)
        subs_lst = [[subt.text.encode('utf-8'),
                     subt.start.to_time(),
                     subt.end.to_time(),
                     'continue']
                    for subt in subs]
        for sub1, sub2 in cls.pairwise(subs_lst):
            # mark 'break' if second subtitle doesn't begin
            # where the first ends
            if sub1[cls.END] != sub2[cls.START]:
                sub1[cls.LINE] = 'break'
<<<<<<< HEAD
        return subs_lst
=======
                return subs_lst
>>>>>>> d770ce59837f9c22a0f95409feb04b480a4158ee

    @classmethod
    def slicebreaks(cls, srtlst):
        """slices an srt list of subtitles by marked 'break's

        """
        breaks = [i + 1 for i, subt
                  in enumerate(srtlst)
                  if subt[cls.LINE] == 'break']
        starts, breaks = [0] + breaks, breaks + [len(srtlst)]
        return [slice(a, b) for a, b in zip(starts, breaks)]

    def infotoparas(self, srtlst):
        """Return pretty formatted paragraphs from a list of subtitles.

        Breaks in time between subtitles define paragraph breaks. TextWrapper
        is used to format the text.
        """
        paras = []
        # iterate by slices defined by 'break's
        for slc in self.slicebreaks(srtlst):
            subs = srtlst[slc]
            text = [subt[self.TEXT].decode('utf-8') for subt in subs]
            # keep beginning and end time of paragraph
            start, end = subs[0][self.START], subs[-1][self.END]
            # use the text wrapper here to create nicely formatted lines
            paras += [(self.wrapper.wrap(u' '.join(text)), start, end)]
<<<<<<< HEAD
        return paras
=======
            return paras
>>>>>>> d770ce59837f9c22a0f95409feb04b480a4158ee

    @staticmethod
    def write_period(start, end):
        fmt = u'%H:%M:%S'
        period = start.strftime(fmt) + u' - ' + end.strftime(fmt)
        return u'_(' + period + u')_'

    @classmethod
    def write_paras(cls, paras):
        """Write paragraphs to stdout.
        """
        for para in paras:
            period = cls.write_period(para[1], para[2])
            print(u'\n' + period + u'\n')
            for line in para[0]:
                print(line)

    @staticmethod
    def get_dups(mylist):
        """get duplicates in a list.

        This is slightly modified from a stack overflow question:
        http://goo.gl/ldgKCk
        .../questions/11236006/identify-duplicate-values-in-a-list-in-python
        """
        d = collections.defaultdict(list)
        for i, item in enumerate(mylist):
            d[item].append(i)
<<<<<<< HEAD
        firsts = [v[0] for k, v in d.items()]
        firsts.sort()
        return(firsts)
=======
            firsts = [v[0] for k, v in d.items()]
            firsts.sort()
            return(firsts)
>>>>>>> d770ce59837f9c22a0f95409feb04b480a4158ee

    @staticmethod
    def format_header(level, num, title, base=1):
        atx_hdr = u'#' * (base + level)
        header_str = u' {0} {1} '.format(num, title)
        return(atx_hdr + header_str + atx_hdr)

    @classmethod
    def header_str(cls, headers):
        header_strs = [[cls.format_header(level, num, title)
                        for level, num, title in header]
                       for header in headers]
        return header_strs

    def print_md(self, base=1):
        """Print a md file of subtitle transcripts.
        """
        # get a list of srt files and folder hierarchy
<<<<<<< HEAD
        srts = self.get_filelist(self.title_dir + u'/' + self.srt_path)
=======
        srts = self.get_filelist(self.title_dir + u'/' + self.path)
>>>>>>> d770ce59837f9c22a0f95409feb04b480a4158ee

        # converting folder names to header names
        hdrs, srt_fs = zip(*srts)
        # get positions of duplicated headers in hierarchy
        headerpos = [self.get_dups(hdr) for hdr in zip(*hdrs)]

        # create header titles
        header_strs = [[self.format_header(j, header[j][0],
                                           header[j][1], base=base)
                        for j, hlevel in enumerate(headerpos) if i in hlevel]
                       for i, header in enumerate(hdrs)]

        # print headers, followed by subtitles
        for headers, srt_file in zip(header_strs, srt_fs):
            print(u'\n' + u'\n\n'.join(headers))
            srtlst = self.srttolist(srt_file)
            paras = self.infotoparas(srtlst)
            self.write_paras(paras)

os.chdir("/home/jowalski/courses/mlfound/ml-foundations/")
title_dir = "04_clustering-and-similarity-retrieving-documents"

cs = Courscript(title_dir)
cs.print_md()
