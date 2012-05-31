"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
APP_NAME = 'OrderApp'
VERSION = '0.0.1'
DATA_FILES = []
PLIST = dict(
            CFBundleName = APP_NAME,
            CFBundleShortVersionString = VERSION,
            CFBundleGetInfoString = "{} {}".format(APP_NAME, VERSION),
            CFBundleExecutable = APP_NAME,
            CFBundleIdentifier = "com.bmbr.order-app")
OPTIONS = dict(
            argv_emulation = True,
            #iconfile = '',
            packages = 'wx',
            site_packages = True,
            plist = PLIST)

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
