from courscript.iter import CourseIter, CourseraWalker
import re
import sys
from functools import singledispatch
from courscript.para import Paralist


class CourseTitle:

    def __init__(self, obj, split="_", sub="-"):
        """
        """
        self.index, self.title = split_num(obj, split, sub)
        self.fmt = "{index}: {title}"

    @property
    def text(self):
        return self.title if self.index is None else \
            self.fmt.format(index=self.index, title=self.title)

    def header(self, level=1):
        atx_str = u'#' * level
        return u'{0} {1} {0}'.format(atx_str, self.text)


def split_num(s, split="_", sub="-"):
    try:
        num, title = re.split(split, s, maxsplit=1)
        num = int(num)
    except ValueError:
        num, title = None, s
    return num, to_title(title, sub)


def to_title(s, sub="-"):
    return re.sub(sub, " ", s).title()


@singledispatch
def write(obj, sobj=None, ssobj=None, sssobj=None, fout=sys.stdout):
    print(CourseTitle(obj.name).header(CourseIter.order[type(obj)]),
          end="\n\n", file=fout)


@write.register(CourseIter.CourseResource)
def write_res(resource, lecture=None, sobj=None, ssobj=None, fout=sys.stdout):
    print_link(resource.title + resource.fmt, resource.url, fout)
    if resource.fmt.endswith("srt"):
        Paralist(CourseraWalker.resource_path(resource, lecture)).print(fout)


def print_link(name, url, fout):
    print("[{}]({})".format(name, url), end="\n\n", file=fout)
