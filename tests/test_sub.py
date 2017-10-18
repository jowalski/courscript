#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pysrt.srtitem import SubRipItem
from pysrt.srttime import SubRipTime
from courscript.sub import SubFile, Sub
from courscript.iter import CourseraWalker
from courscript.write import CourseTitle
from courscript.para import Para, Paralist
import datetime
import pysrt
import os
# import codecs

# file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, os.path.abspath(file_path))

test_dir = "tests"
test_subfile = os.path.join(
    test_dir, "cryptocurrency", "lectures",
    "02_how-bitcoin-achieves-decentralization",
    "01_how-bitcoin-achieves-decentralization",
    "01_01_centralization-vs-decentralization.en.srt")


class TestSubtitle(unittest.TestCase):

    def test_subtitle(self):
        subtitle_text = "hello"
        subtitle_start = SubRipTime(0, 0, 0, 0)
        subtitle_end = SubRipTime(0, 0, 1, 0)
        subtitle = Sub(SubRipItem(index=0, start=subtitle_start,
                                  end=subtitle_end, text=subtitle_text))
        self.assertEqual(subtitle.text, subtitle_text)
        self.assertEqual(subtitle.start, subtitle_start)
        self.assertEqual(subtitle.end, subtitle_end)
        self.assertEqual(subtitle.ftext, subtitle_text.encode('utf-8'))
        self.assertEqual(subtitle.fstart, datetime.time(0, 0, 0, 0))
        self.assertEqual(subtitle.fend, datetime.time(0, 0, 1, 0))

    def test_read_subtitle(self):
        # note: this produces a "DeprecationWarning: 'U' mode" warning,
        # from the codecs.open call in pysrt._open_unicode_file
        subtitle_read = Sub(pysrt.open(test_subfile)[0])
        self.assertEqual(subtitle_read.ftext, b'[MUSIC]')
        self.assertEqual(subtitle_read.fstart, datetime.time(0, 0, 0, 340000))
        self.assertEqual(subtitle_read.fend, datetime.time(0, 0, 10, 340000))


class TestMultipleSubtitles(unittest.TestCase):

    def setUp(self):
        # with codecs.open(self.test_subfile, encoding='utf-8') as f:
        #     self.test_srt = pysrt.stream(f)
        #     self.subtitle = Sub(next(self.test_srt))
        #     self.next_subtitle = Sub(next(self.test_srt))
        #     self.last_subtitle = Sub(next(self.test_srt))
        self.subtitle, self.next_subtitle, self.last_subtitle = \
            [Sub(subt) for subt in pysrt.open(test_subfile)[0:3]]
        # self.next_subtitle = Sub(next(self.test_srt))
        # self.last_subtitle = Sub(next(self.test_srt))

    def test_sub_break(self):
        self.assertTrue(self.subtitle.is_break(self.next_subtitle))
        self.assertFalse(self.next_subtitle.is_break(self.last_subtitle))

    def test_subgroup(self):
        subfile = SubFile(test_subfile)
        subgroup = list(subfile.group_subs(subfile.subiter))[1]
        self.assertEqual(subgroup.start, datetime.time(0, 0, 16, 20000))
        self.assertEqual(subgroup.end, datetime.time(0, 1, 11, 850000))

    def test_subfile(self):
        subfile = SubFile(test_subfile)
        self.assertEqual(len(list(subfile)), 5)


class TestPara(unittest.TestCase):

    def setUp(self):
        self.subfile = SubFile(test_subfile)
        self.grouplist = list(self.subfile.group_subs(self.subfile.subiter))
        self.subgroup = self.grouplist[1]

    def test_para(self):
        para = Para(self.subgroup)
        self.assertEqual(para.data[0:10], "Hello, and")

    def test_para_wrap_len(self):
        para = Para(self.subgroup)
        self.assertEqual(len(para.data), 1006)


class TestParalist(unittest.TestCase):

    def test_paralist(self):
        self.assertEqual(len(Paralist(test_subfile)), 5)


class TestCourseWalker(unittest.TestCase):

    def setUp(self):
        self.syllabus_file = "cryptocurrency-syllabus-parsed.json"
        self.coursename = "cryptocurrency"
        self.subdir = "lectures"
        self.module_name = "01_introduction-to-crypto-and-cryptocurrencies"
        self.section_path = os.path.join(
            test_dir, self.coursename, self.subdir, self.module_name,
            self.module_name)
        self.first_resource_path = os.path.join(self.section_path,
                                                "01_01_welcome.en.srt")

    def create_walker(self):
        return CourseraWalker(self.coursename,
                              os.path.join(test_dir, self.syllabus_file),
                              subdir=self.subdir,
                              path=test_dir,
                              formats=["srt"])

    def test_walker_iters(self):
        walker = self.create_walker()
        self.assertEqual(len(list(walker.walk_modules())), 61)
        self.assertEqual(len(list(walker.iter_modules())), 12)

    def test_coursera_walker(self):
        walker = self.create_walker()
        iter = walker.walk_modules()
        module, section, lecture, resource = next(iter)
        self.assertEqual(module.name, self.module_name)
        self.assertEqual(section.dir, self.section_path)
        self.assertEqual(walker.resource_path(resource, lecture),
                         self.first_resource_path)

    def test_coursetitle(self):
        title = CourseTitle("1_abc-def-hij")
        self.assertEqual(title.text, "1: Abc Def Hij")
        self.assertEqual(title.index, 1)
        self.assertEqual(title.title, "Abc Def Hij")


class TestTitle(unittest.TestCase):

    def setUp(self):
        self.title_str = "1_abc-def"
        self.title = "Abc Def"
        self.index = 1

    def test_title(self):
        title = CourseTitle(self.title_str)
        self.assertEqual(title.text, "{}: {}".format(self.index, self.title))
        self.assertEqual(title.title, self.title)
        self.assertEqual(title.index, self.index)
