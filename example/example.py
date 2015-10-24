import os
from courscript import Courscript
from folder import CourseFilelist
from header import CourseHeaderList
from sub import CourseSublist
from para import CourseParalist


os.chdir("/home/jowalski/courses/mlfound/ml-foundations/")
title_dir = "04_clustering-and-similarity-retrieving-documents"


cs = Courscript(title_dir)
srts = CourseFilelist(title_dir, "*/*.srt")
headerlist = CourseHeaderList(srts, 1)
srtlst = CourseSublist(srts[0].path)
paras = CourseParalist(srtlst, headerlist[0])
# cs.print_md()

clust_file = open('04_clustering.md', 'w')
cs.print(clust_file)
clust_file.close()
