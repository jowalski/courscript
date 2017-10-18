from courscript.iter import CourseIter, CourseraWalker
import re
import sys
import os
from functools import singledispatch, partial
from courscript.para import Paralist


class CourseTitle:

    FMT = "{index}: {title}"

    def __init__(self, obj, split="_", sub="-"):
        """
        """
        self.index, self.title = self._split_num(obj, split, sub)

    @property
    def text(self):
        return self.title if self.index is None else \
            self.FMT.format(index=self.index, title=self.title)

    def as_header(self, level=1):
        return self.header(self.text, level=level)

    @staticmethod
    def header(text, level=1):
        atx_str = u'#' * level
        return u'{0} {1} {0}'.format(atx_str, text)

    @classmethod
    def _split_num(cls, s, split="_", sub="-"):
        try:
            num, title = re.split(split, s, maxsplit=1)
            num = int(num)
        except ValueError:
            num, title = None, s
        return num, title.replace(sub, " ").title()


prl = partial(print, end="\n\n")


@singledispatch
def write(obj, sobj=None, ssobj=None, sssobj=None, fout=sys.stdout):
    prl(CourseTitle(obj.name).as_header(CourseIter.order[type(obj)]),
        file=fout)


@write.register(CourseIter.CourseResource)
def write_res(resource, lecture=None, sobj=None, ssobj=None, fout=sys.stdout):
    if resource.fmt.endswith("html"):
        print_inline_html(resource, fout)
    else:
        print_link("{}.{}".format(resource.title, resource.fmt),
                   resource.url, fout)
    if resource.fmt.endswith("srt"):
        res_path = CourseraWalker.resource_path(resource, lecture)
        if not os.path.exists(res_path):
            raise FileNotFoundError("Could not find resource: {}".
                                    format(res_path))
        Paralist(res_path).print(fout, srt_escape_filter)


def print_link(name, url, fout):
    prl("[{}]({})".format(name, url), file=fout)


def print_inline_html(resource, fout):
    prl(CourseTitle.header(resource.title.title(),
                           CourseIter.order[type(resource)]),
        file=fout)
    prl(re.sub("^#inmemory#", "", resource.url), file=fout)


def srt_escape_filter(text):
    return str(text).replace("_", "\_")\
                    .replace("*", "\*")\
                    .replace("`", "\`")\
                    .replace("<", "\<")
