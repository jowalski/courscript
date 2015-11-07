import os
from courscript import Courscript
from folder import CourseFilelist
from header import HeaderList
from sub import Sublist
from para import Paralist


os.chdir("/home/jowalski/courses/mlfound/ml-foundations/")
title_dir = "04_clustering-and-similarity-retrieving-documents"


cs = Courscript(title_dir)
srts = CourseFilelist(title_dir, "*/*.srt")
headerlist = HeaderList(srts, 1)
srtlst = Sublist(srts[0].path)
paras = Paralist(srtlst, headerlist[0])
# cs.print_md()

clust_file = open('04_clustering.md', 'w')
cs.print(clust_file)
clust_file.close()

