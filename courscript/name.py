import reprlib
import re


class CourseName:

    def __init__(self, path, split, sub):
        self.path = path
        try:
            self.num, self.name = re.split(split, path, maxsplit=1)
            try:
                self.num = int(self.num)
            except ValueError:
                self.num = int(re.findall('^[0-9]+', self.num)[0])
        except ValueError:
            # FIXME: just a hack to parse nlp class & others properly
            self.num = int(re.findall('^[0-9]+', path)[0])
            path1 = re.sub('^[0-9]+_', '', path)
            self.name = re.sub('_[0-9-]+$', '', path1)
        try:
            self.name, self.ext = re.split('\.', self.name)
        except ValueError:
            self.ext = ''
        self.name = re.sub(sub, ' ', self.name).title()

    def __str__(self):
        return('{}: {}'.format(int(self.num), self.name))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__,
                               reprlib.repr(self.__str__()))

    # def __hash__(self):
    #     return hash(self.path)

    # def __eq__(self, other):
    #     return self.path == other.path

    def __lt__(self, other):
        if hasattr(self, 'num') and hasattr(other, 'num'):
            return self.num < other.num
        else:
            return self.path < other.path

    def __gt__(self, other):
        return self.__lt__(other)
