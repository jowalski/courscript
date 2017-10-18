courscript
===============

courscript is a Python library for creating readable documents from video
subtitle files.

Intro
===============

For now courscript uses the pysrt library to read .srt or .vtt files. The target
audience is viewers of online courses, it is often helpful to have a text
transcript, perhaps _more_ useful for some than watching and listening.

Usage
===============

::

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
