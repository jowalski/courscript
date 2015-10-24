import collections
import reprlib


class CourseHeaderList:

    def __init__(self, filelist, base=1):
        self.base = base
        self.headers = self._from_filelist(filelist)

    def __getitem__(self, position):
        return self.headers[position]

    def __repr__(self):
        values = ', '.join('{!r}'.format(i) for i in self.headers)
        return '{}({})'.format(self.__class__.__name__, values)

    def _from_filelist(self, filelist):
        # get positions of duplicated headers in hierarchy
        headerpos = [self.get_dups(hdr) for hdr in filelist.by_units()]

        # create header titles
        header_strs = [[CourseHeader(header.units[j], self.base + j)
                        for j, hlevel in enumerate(headerpos) if i in hlevel]
                       for i, header in enumerate(filelist)]
        return header_strs

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
        firsts = [v[0] for k, v in d.items()]
        firsts.sort()
        return(firsts)


class CourseHeader:

    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __str__(self):
        atx = u'#' * self.level
        return u'{0} {1} {0}'.format(atx, self.name)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__,
                               reprlib.repr(self.__str__()))
