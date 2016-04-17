import docopt
import os.path
import sys
import pypandoc
from courscript.courscript import Courscript


class CourscriptCLI:
    def __init__(self):
        self._entry()

    def _entry(self):
        doc_str = """

    Usage: courscript [-h] <FOLDER> <FILE_OUT> [options]

    Convert srt files in FOLDER (at some level, not necessarily the first)
    into a nicely formatted markdown document.

    Arguments:
      FOLDER       folder name
      FILE_OUT     name of output markdown file name

    Options:
      -h --help
      -l split --split=split    split filename pattern [default: _]
      -s sub --sub=sub          sub filename pattern [default: -]
      -p path --path=path       srt file paths [default: */*.srt]
      -d slides --slides=sld    pdf slide file paths
      -t html --html            output html file
      -c css --css=css          css style sheet to go with html
        """
        args = docopt.docopt(doc_str, version='courscript version 0.1')

        folder = args['<FOLDER>']
        if not os.path.isdir(folder):
            exit('{} is not a folder'.format(folder))
        # print(args)
        self.cs = Courscript(args['<FOLDER>'], args['--path'], 1,
                             args['--split'], args['--sub'],
                             args['--slides'])
        with open(args['<FILE_OUT>'], 'w') as f:
            self.cs.print(f)
        if args['--html']:
            pandoc_args = ['-s', '--self-contained']
            if args['--css']:
                pandoc_args += ['-c {css}'.format(css=args['css'])]
            md_file = args['<FILE_OUT>']
            html_file = '{}.html'.format(os.path.splitext(md_file)[0])
            pypandoc.convert(args['<FILE_OUT>'], 'html', extra_args=pandoc_args,
                             outputfile=html_file)
        sys.exit()
