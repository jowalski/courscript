import os
import coursera.workflow
from coursera.utils import normalize_path
import configargparse as argparse
import json


class CourseraWalker:

    def __init__(self, coursename, syllabus_file, path=".",
                 subdir=None, formats=["srt"], combined=True):
        self.path = path
        self.coursename = coursename
        self.subdir = subdir
        self._load_json(syllabus_file)
        self._build_dummy_parser(formats, combined)

    def _load_json(self, syllabus_file):
        with open(syllabus_file) as s_file:
            self.modules = json.load(s_file)

    def _build_dummy_parser(self, formats, combined):
        """
        Each builtin argument provided here is required for _iter_modules.
        """
        self.parser = argparse.ArgParser()
        group_material = self.parser.add_argument_group('download stuff')

        for flag, dest, default in \
            zip(['-f', '-lf', '-rf', '-sf'],
                ['file_formats', 'lecture_filter', 'resource_filter',
                 'section_filter'],
                ['all', None, None, None]):
            group_material.add_argument(flag, dest=dest, default=default)

        for flag, dest, default in \
            zip(['--verbose-dirs', '--combined-section-lectures-nums'],
                ['verbose_dirs', 'combined_section_lectures_nums'],
                [False, combined]):
            self.parser.add_argument(flag, dest=dest, default=default)

        arg_str = "-f \"{}\"".format(" ".join(formats))
        self.args = self.parser.parse_args(arg_str)

    def _subpath(self):
        return os.path.join(self.coursename, self.subdir) if self.subdir \
            else self.coursename

    def __iter__(self):
        return self.walk_modules()

    def walk_modules(self):
        return coursera.workflow._walk_modules(self.modules, self._subpath(),
                                               self.path, None, self.args)

    def iter_modules(self):
        return (CourseIter.CourseModule(module) for module in
                coursera.workflow._iter_modules(self.modules, self._subpath(),
                                                self.path, None, self.args))

    def iter_files(self):
        return (self.resource_path(resource, lecture) for
                module, section, lecture, resource in self)

    def validate_files(self):
        return all(map(os.path.isfile, list(self.iter_files())))

    # [(CourseTitle(module.name).text,
    #   [(CourseTitle(section.name).text,
    #     [(CourseTitle(lecture.name).text,
    #       [(lecture.filename(resource.fmt, resource.title), resource.url)
    #        for resource in lecture.resources])
    #      for lecture in section.lectures])
    #    for section in module.sections])
    #  for module in cwalker.iter_modules()]

    def apply(self, f):
        for module in self.iter_modules():
            f(module)
            for section in module.sections:
                f(section, module)
                for lecture in section.lectures:
                    f(lecture, section, module)
                    for resource in lecture.resources:
                        f(resource, lecture, section, module)

    @staticmethod
    def resource_path(resource, lecture):
        return normalize_path(lecture._iter_obj.filename(resource.fmt, resource.title))


class CourseIter:
    """
    ~Metaclass for wrapping IterModule, IterSection, IterLecture,
    and IterResource.

    """

    # class factory: creates a class to wrap an Iter_ object
    def iter_wrapper(cls_name, field_names, iter_fun=None, iter_type=None):
        def __init__(self, iter_obj):
            self._iter_obj = iter_obj

        def iter_attr(attr_name):
            def iter_attr_getter(instance):
                return instance._iter_obj.__dict__[attr_name]
            return property(iter_attr_getter)

        def wrap_iterator(iter_fun_name, sub_iter_class):
            def iter_wrapper_getter(instance):
                return (sub_iter_class(obj)
                        for obj in getattr(instance._iter_obj, iter_fun_name))
            return [] if iter_fun is None \
                else [(iter_fun_name, property(iter_wrapper_getter, None))]

        cls_attrs = dict([(name, iter_attr(name)) for name in field_names] +
                         wrap_iterator(iter_fun, iter_type) +
                         [("__init__", __init__)])

        return type(cls_name, (object,), cls_attrs)

    # wrapped classes
    CourseResource = iter_wrapper("CourseResource", ["title", "fmt", "url"])
    CourseLecture = iter_wrapper("CourseLecture",
                                 ["name", "filename", "index"],
                                 "resources", CourseResource)
    CourseSection = iter_wrapper("CourseSection", ["name", "dir", "index"],
                                 "lectures", CourseLecture)
    CourseModule = iter_wrapper("CourseModule", ["name", "index"],
                                "sections", CourseSection)

    order = {CourseModule: 1,
             CourseSection: 2,
             CourseLecture: 3,
             CourseResource: 4}

    # from courscript.iter import CourseraWalker
    # from courscript.write import write

    # import os
    # os.chdir("/home/jowalski/usbcrypt/courses")
    # cwalker = CourseraWalker("cryptocurrency",
    #                                        "cryptocurrency-syllabus-parsed.json",
    #                                        subdir="lectures")

    # with f as open("test.md", 'w'):

    #     cwalker.apply(lambda a, b=None, c=None, d=None: write(a, b, c, d, fout=f))
