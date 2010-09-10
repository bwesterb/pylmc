#!/usr/bin/env python

from setuptools import setup, find_packages
from get_git_version import get_git_version

setup(name='pylmc',
      version=get_git_version(),
      description='Assembler and interpreter for the Little Man Computer',
      author='Bas Westerbaan',
      classifiers = [
	      'Development Status :: 3 - Alpha',
	      'Environment :: Console',
	      'Intended Audience :: Developers',
	      'Intended Audience :: Education',
	      'License :: OSI Approved :: GNU Affero General Public License v3',
	      'Natural Language :: English',
	      'Operating System :: POSIX',
	      'Operating System :: Microsoft',
	      'Programming Language :: Python :: 2.7',
	      'Topic :: Software Development :: Interpreters',
	      'Topic :: Software Development :: Libraries',
	      'Topic :: Software Development :: Assemblers',
	      'Topic :: Software Development :: Code Generators',
	      'Topic :: Software Development :: Disassemblers'
      ],
      author_email='bas@westerbaan.name',
      url='http://github.com/bwesterb/pylmc/',
      packages=['lmc'],
      zip_safe=True,
      package_dir={'lmc': 'src'},
      entry_points = {
	      'console_scripts': [
		      'lmca = lmc.assembler:main',
		      'lmc = lmc.interpreter:main',
	      ],
      }
      )
