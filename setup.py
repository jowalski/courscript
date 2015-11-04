#!/usr/bin/env python

from setuptools import setup, find_packages

# https://packaging.python.org/en/latest/distributing/#working-in-development-mode
setup(name='courscript',
      version='0.1',
      description='Generate readable documents from course video subtitles',
      url='http://github.com/jowalski/courscript',
      author='John Kowalski',
      author_email='jowalski@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['pysrt'],
      entry_points={
          'console_scripts': [
              'courscript = courscript.cli:CourscriptCLI'
          ]},
      keywords="subtitle course coursera srt",
      platforms=["Independent"],
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Education',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',  # ??
          'Programming Language :: Python :: 3.4',
          'Topic :: Education',
          'Topic :: Multimedia :: Video :: Conversion',
          'Topic :: Text Processing :: Markup'])
