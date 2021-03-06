import glob
import os.path
import os
import subprocess
import shutil
import re
from courscript.error import CoursError
from courscript.folder import CourseFilelist


class CoursePdflist:

    def __init__(self, base_dir, path, split, sub):
        self.path = path
        self.pdffiles = CourseFilelist(base_dir, path, split, sub)
        self.pdflist = [CoursePdf(pdf) for pdf in self.pdffiles]

    def __getitem__(self, key):
        return self.pdflist[key]


class CoursePdf:

    def __init__(self, cfile):
        self.cfile = cfile
        self.slist = CourseSlidelist(cfile)


class CourseSlidelist:
    PDF_CONV_PROG = 'pdf2svg'

    def __init__(self, cfile):
        self.cfile = cfile
        self.pdfpath = cfile.path
        self.pdfdir = os.path.split(self.pdfpath)[0]
        self.filename = os.path.basename(os.path.splitext(self.pdfpath)[0])
        self.make_slides()

    def __len__(self):
        return len(self.slist)

    def __getitem__(self, position):
        return self.slist[position]

    def make_slides(self):
        # this is a CourseName
        cname = self.cfile.names[1]
        safe_fname = '{}_{}'.format(cname.num, cname.name)
        safe_fname = re.sub('[^a-zA-Z0-9]', '', safe_fname)
        self.slidefolder = os.path.join(self.pdfdir, safe_fname)
        try:
            os.mkdir(self.slidefolder)
        except FileExistsError:
            spaths = glob.glob('{}/*.svg'.format(self.slidefolder))
            if len(spaths) == 0:
                shutil.rmtree(self.slidefolder)
                err = 'Folder {} exists but there are no slides. Removed'
                raise CoursError(err.format(self.slidefolder))
        else:
            spath = os.path.join(self.slidefolder,
                                 '{}_slide%d.svg'.format(safe_fname))
            print('Making slides for {}...'.format(self.filename))
            subprocess.check_call([self.PDF_CONV_PROG, self.pdfpath,
                                   spath, 'all'])
            spaths = glob.glob('{}/*.svg'.format(self.slidefolder))
        self.slist = [CourseSlide(path, cname.name, cname.num, len(spaths))
                      for path in spaths]
        self.slist.sort()

    def delete_slides(self):
        shutil.rmtree(self.slidefolder)
        self.slidepaths = []


class CourseSlide:

    def __init__(self, path, unitname, unitnum, numof):
        self.path = path
        self.unitname = unitname
        self.unitnum = unitnum
        self.numof = numof
        self.num = int(re.findall('[0-9]+', path)[-1])

    def __str__(self):
        return '{unitnum} {name} Slide {num} of {numof}'.\
            format(unitnum=self.unitnum, name=self.unitname,
                   num=self.num, numof=self.numof)

    def __lt__(self, other):
        return self.num < other.num

    def __gt__(self, other):
        return self.num > other.num
