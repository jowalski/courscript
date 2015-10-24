import re
import os.path
import glob
import reprlib


class CourseFilelist:

    def __init__(self, folder, search_path):
        self.folder, self.search_path = folder, search_path
        self.filelist = self._make_filelist(os.path.join(folder, search_path))

    def __getitem__(self, position):
        return self.filelist[position]

    def __repr__(self):
        values = ', '.join('{!r}'.format(i) for i in self.filelist)
        return '{}({})'.format(self.__class__.__name__, values)

    def _make_filelist(cls, pattern):
        """Get a list of files from globbing a pattern, including parsed title info.

        Parsed info includes section, lecture number and title info.
        """
        return [CourseFile(srt) for srt in glob.glob(pattern)]

    def by_units(self):
        return([unit for unit in
                zip(*[cfile.units for cfile in self.filelist])])


class CourseUnit:

    def __init__(self, path):
        self.path = path
        self.num, self.name = re.split('_', path)
        try:
            self.name, self.ext = re.split('\.', self.name)
        except ValueError:
            self.ext = ''
        self.name = re.sub('-', ' ', self.name).title()

    def __str__(self):
        return('{}: {}'.format(int(self.num), self.name))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__,
                               reprlib.repr(self.__str__()))

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        return self.path == other.path


class CourseFile:

    def __init__(self, path):
        self.path = path
        self.units = self.parse(path)

    def __str__(self):
        return(self.path)

    def __repr__(self):
        return('CourseFile({})'.format(reprlib.repr(self.path)))

    @classmethod
    def parse(cls, path):
        """Parse a path string recursively into a list of CourseUnits.
        """
        head, tail = os.path.split(path)
        tail_lst = [CourseUnit(tail)]
        if not head:
            return tail_lst
        return(cls.parse(head) + tail_lst)
