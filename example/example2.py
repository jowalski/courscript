import os
from courscript import Courscript
from folder import CourseFilelist
from header import CourseHeaderList
from sub import CourseSublist
from para import CourseParalist
from slide import CoursePdflist

os.chdir("/home/jowalski/courses/nlpintro/nlpintro-001")
title_dir = "01_Week_One_Introduction_1-2_1-35-31"
srts = CourseFilelist(title_dir, "*.srt")
headerlist = CourseHeaderList(srts,1)
srtlst = Sublist(srts[0].path)
paras = Paralist(srtlst, headerlist[0])

