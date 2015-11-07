import os.path
import reprlib
from courscript.name import CourseName
import glob


class CourseFilelist:

    def __init__(self, folder, search_path, split, sub):
        self.folder = folder
        self.search_path = search_path
        self.filelist = [CourseFile(srt, split, sub)
                         for srt in
                         glob.glob(os.path.join(folder, search_path))]

    def __getitem__(self, position):
        return self.filelist[position]

    def __repr__(self):
        values = ', '.join('{!r}'.format(i) for i in self.filelist)
        return '{}({})'.format(self.__class__.__name__, values)

    def by_names(self):
        return([unit for unit in
                zip(*[cfile.names for cfile in self.filelist])])


class CourseFile:

    def __init__(self, path, split, sub):
        self.path = path
        self.names = self.parse(path, split, sub)

    def __str__(self):
        return(self.path)

    def __repr__(self):
        return('CourseFile({})'.format(reprlib.repr(self.path)))

    @classmethod
    def parse(cls, path, split, sub):
        """Parse a path string recursively into a list of CourseNames.
        """
        head, tail = os.path.split(path)
        tail_lst = [CourseName(tail, split, sub)]
        if not head:
            return tail_lst
        return(cls.parse(head, split, sub) + tail_lst)
