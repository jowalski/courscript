import docopt
import os.path
import sys
import pypandoc
import re
from functools import partial
from courscript.iter import CourseraWalker
from courscript.write import write


class CourscriptCLI:
    SYLLABUS_SUFFIX = "-syllabus-parsed.json"
    SYLLABUS_FILE_ERROR = "syllabus file name invalid"

    def __init__(self):
        self._run()

    def _run(self):
        doc_str = """

    Usage: courscript [-h] <SYLLABUS> [options]

    Convert srt files in course folder into a nicely formatted
    markdown document.

    Arguments:
      SYLLABUS     syllabus file (json)

    Options:
      -h --help
      -n cname --cname          course name
      -p path --path=path       base path [default: .]
      -s subdir --subdir=sdir   sub-directory in course folder
      -f fmts --fmts            resource formats to use [default: srt]
      -o out --out              output file
      -d slides --slides=sld    pdf slide file paths
      -t html --html            output html file
      -c css --css=css          css style sheet to go with html
        """
        args = docopt.docopt(doc_str, version='courscript version 0.2')

        syllabus = args['<SYLLABUS>']
        coursename = self.extract_coursename(syllabus) \
            if args["--cname"] is None else args["--cname"]

        self.cw = CourseraWalker(coursename, syllabus, args["--path"],
                                 args["--subdir"],
                                 re.split(" +", args["--fmts"]), True)

        outname = args["--out"]
        with (sys.stdout if outname is None else open(outname, 'w')) as f:
            self.cw.apply(partial(write, fout=f))
        if args['--html']:
            pandoc_args = ['-s', '--self-contained']
            if args['--css']:
                pandoc_args += ['-c {css}'.format(css=args['css'])]
            # md_file = args['<FILE_OUT>']
            html_file = '{}.html'.format(os.path.splitext(outname)[0])
            pypandoc.convert(outname, 'html', extra_args=pandoc_args,
                             outputfile=html_file)
        sys.exit()

    @staticmethod
    def extract_coursename(syllabus_path):
        basename = os.path.basename(syllabus_path)
        if basename.endswith(CourscriptCLI.SYLLABUS_SUFFIX):
            return basename.replace(CourscriptCLI.SYLLABUS_SUFFIX, "")
        else:
            raise FileNotFoundError(CourscriptCLI.SYLLABUS_FILE_ERROR)
