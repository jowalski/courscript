import docopt
import os.path
from courscript.courscript import Courscript


class CourscriptCLI:
    def __init__(self):
        self._entry()

    def _entry(self):
        doc_str = """
        Usage: courscript [-vqrh] <FOLDER> [--path=<path>] <FILE_OUT>

        Convert srt files in FOLDER (at some level, not necessarily the first)
        into a nicely formatted markdown document.

        Arguments:
          FOLDER       folder name
          FILE_OUT     name of output markdown file name

        Options:
          -h --help
          -v           verbose mode
          -q           quiet mode
          -r           make report
          --path=path  srt file paths [default: */*.srt]

        """
        args = docopt.docopt(doc_str, version='courscript version 0.1')

        folder = args['<FOLDER>']
        if not os.path.isdir(folder):
            exit('{} is not a folder'.format(folder))
        if '--path' in args:
            self.cs = Courscript(folder, args['--path'])
        else:
            self.cs = Courscript(folder)
        with open(args['<FILE_OUT>'], 'w') as f:
            self.cs.print(f)
