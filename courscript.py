import os
import glob
import re
import pysrt
import itertools
import textwrap
import collections


def parse_fdname(dirname):
    """Split a file or directory name into component parts.

    This at least works for coursera, the ml-foundations course hierarchy.
    """
    num, name = re.split('_', dirname)
    try:
        title, ext = re.split('\.', name)
    except ValueError:
        return int(num), re.sub('-', ' ', name)
    return int(num), re.sub('-', ' ', title), ext


# itertools.starmap(os.path.split)

def parse_srt_path(path):
    """Parse a path string into a tuple using os.path.split recursively.
    """
    head, tail = os.path.split(path)
    tail_lst = [parse_fdname(tail)]
    if not head:
        return tail_lst
    return(parse_srt_path(head) + tail_lst)


def get_filelist(pattern):
    """Get a list of files from globbing a pattern, including parsed title info.

    Parsed info includes section, lecture number and title info.
    """
    filelist = [(parse_srt_path(srt), srt) for srt in glob.glob(pattern)]
    return filelist


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

TEXT, START, END, LINE = 0, 1, 2, 3


def srttolist(file):
    """Convert srt subtitle file to list of subtitle elements.

    Each element consists of [text, start, end, 'continue'/'break'] fields.
    """
    subs = pysrt.open(file)
    subs_lst = [[subt.text.encode('utf-8'),
                 subt.start.to_time(),
                 subt.end.to_time(),
                 'continue']
                for subt in subs]
    for sub1, sub2 in pairwise(subs_lst):
        # mark 'break' if second subtitle doesn't begin where the first ends
        if sub1[END] != sub2[START]:
            sub1[LINE] = 'break'
    return subs_lst


def slicebreaks(srtlst):
    """slices an srt list of subtitles by marked 'break's

    """
    breaks = [i + 1 for i, subt
              in enumerate(srtlst)
              if subt[LINE] == 'break']
    starts, breaks = [0] + breaks, breaks + [len(srtlst)]
    return [slice(a, b) for a, b in zip(starts, breaks)]

wrapper = textwrap.TextWrapper()


def infotoparas(srtlst):
    """Return pretty formatted paragraphs from a list of subtitles.

    Breaks in time between subtitles define paragraph breaks. TextWrapper
    is used to format the text.
    """
    paras = []
    # iterate by slices defined by 'break's
    for slc in slicebreaks(srtlst):
        subs = srtlst[slc]
        text = [subt[TEXT].decode('utf-8') for subt in subs]
        # keep beginning and end time of paragraph
        start, end = subs[0][START], subs[-1][END]
        # use the text wrapper here to create nicely formatted lines
        paras += [(wrapper.wrap(u' '.join(text)), start, end)]
    return paras


def write_period(start, end):
    fmt = u'%H:%M:%S'
    period = start.strftime(fmt) + u' - ' + end.strftime(fmt)
    return u'_(' + period + u')_'


def write_paras(paras):
    """Write paragraphs to stdout.
    """
    for para in paras:
        period = write_period(para[1], para[2])
        print(u'\n' + period + u'\n')
        for line in para[0]:
            print(line)


def write_headers(headers, base_lev=2):
    """Write headers to stdout.
    """
    for i, hdr in enumerate(headers):
        atx_hdr = u'#' * (base_lev + i)
        title_str = u'{0} {1} - {2} {0}'.format(atx_hdr, hdr[0], hdr[1])
        print(u'\n' + title_str + u'\n')


def get_dups(mylist):
    """get duplicates in a list.

    Slightly modified from stack overflow:
    http://goo.gl/ldgKCk
    .../questions/11236006/identify-duplicate-values-in-a-list-in-python
    """
    d = collections.defaultdict(list)
    for i, item in enumerate(mylist):
        d[item].append(i)
    firsts = [v[0] for k, v in d.items()]
    firsts.sort()
    return(firsts)


def format_header(level, num, title, base=1):
    atx_hdr = u'#' * (base + level)
    header_str = u' {0} {1} '.format(num, title)
    return(atx_hdr + header_str + atx_hdr)


def header_str(headers):
    header_strs = [[format_header(level, num, title)
                    for level, num, title in header]
                   for header in headers]
    return header_strs


def print_md(folder, path="*/*.srt", base=1):
    """Print a md file of subtitle transcripts.
    """
    num, title = parse_fdname(folder)
#    print(format_header(0, num, title, 1) + u'\n')

    # get a list of srt files and folder hierarchy
    srts = get_filelist(folder + u'/' + path)

    # converting folder names to header names
    hdrs, srt_fs = zip(*srts)
    # get positions of duplicated headers in hierarchy
    headerpos = [get_dups(hdr) for hdr in zip(*hdrs)]
    # create header titles
    header_strs = [[format_header(j, header[j][0], header[j][1], base=base)
                    for j, hlevel in enumerate(headerpos) if i in hlevel]
                   for i, header in enumerate(hdrs)]

    # print headers, followed by subtitles
    for headers, srt_file in zip(header_strs, srt_fs):
        print(u'\n' + u'\n\n'.join(headers))
        srtlst = srttolist(srt_file)
        paras = infotoparas(srtlst)
        write_paras(paras)

ex_dir = "04_clustering-and-similarity-retrieving-documents"

os.chdir("/home/jowalski/courses/mlfound/ml-foundations/")

print_md(ex_dir)
