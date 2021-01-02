# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt5. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt5app.py is a very simple type of PyQt5 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': [],
        'packages': [],
        'include_files': ['./Icons/photo.jpg', './Icons/gear.png', './Icons/Information_16x16.png', './Icons/upload.png',
                          './Icons/windowIcon.png','./Icons/check.png','./Icons/Log Out_16x16.png','./Icons/Open_16x16.png','./Icons/home.png','./Icons/Cancel_16x16.png'],
    }
}

executables = [
    Executable('ReportBuilderAR.py', icon='./Icons/windowIcon.ico', base=base)
]

setup(name='ReportBuilder',
      version='1.0.0',
      description='',
      options=options,
      executables=executables
      )
