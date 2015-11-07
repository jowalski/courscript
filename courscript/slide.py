import glob
import os.path
import os
import subprocess
import shutil
import re
from courscript.error import CoursError


class CoursePdflist:

    def __init__(self, base_dir, path):
        self.path = path
        self.pdflist = [CoursePdf(pdf) for pdf in
                        glob.glob(os.path.join(base_dir, path))]

    def __getitem__(self, key):
        return self.pdflist[key]


class CoursePdf:

    def __init__(self, path):
        self.path = path
        self.slist = CourseSlidelist(path)


class CourseSlidelist:
    PDF_CONV_PROG = 'pdf2svg'

    def __init__(self, pdfpath):
        self.pdfpath = pdfpath
        self.pdfdir = os.path.split(pdfpath)[0]
        self.filename = os.path.basename(os.path.splitext(pdfpath)[0])
        self.make_slides()

    def __len__(self):
        return len(self.slist)

    def __getitem__(self, position):
        return self.slist[position]

    def make_slides(self):
        safe_fname = re.sub('[^A-Za-z0-9]', '', self.filename)
        self.slidefolder = os.path.join(self.pdfdir, safe_fname)
        try:
            os.mkdir(self.slidefolder)
        except FileExistsError:
            spaths = glob.glob('{}/*.svg'.format(self.slidefolder))
            if len(spaths) == 0:
                shutil.rmtree(self.slidefolder)
                raise CoursError("""Folder {} exists but there
                                    are no slides. Removed.
                                 """
                                 .format(self.slidefolder))
            self.slist = [CourseSlide(path, i, len(spaths), safe_fname)
                          for i, path in enumerate(spaths)]
        else:
            spath = os.path.join(self.slidefolder,
                                 '{}_slide%d.svg'.format(safe_fname))
            print('Making slides for {}...'.format(self.filename))
            subprocess.check_call(['pdf2svg', self.pdfpath, spath, 'all'])
            spaths = glob.glob('{}/*.svg'.format(self.slidefolder))
            l = len(spaths)
            self.slist = [CourseSlide(path, i, l, safe_fname)
                          for i, path in enumerate(spaths)]

    def delete_slides(self):
        shutil.rmtree(self.slidefolder)
        self.slidepaths = []


class CourseSlide:

    def __init__(self, path, num, numof, pdfname):
        self.path = path
        self.num = num
        self.numof = numof
        self.pdfname = pdfname

    def __str__(self):
        return '{} Slide {} of {}'.\
            format(self.pdfname, self.num + 1, self.numof)
