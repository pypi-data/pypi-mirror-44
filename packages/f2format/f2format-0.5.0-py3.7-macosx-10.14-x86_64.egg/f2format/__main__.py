# -*- coding: utf-8 -*-

import argparse
import locale
import os
import shutil
import sys
import uuid
import warnings

from f2format.core import f2format

# multiprocessing may not be supported
try:        # try first
    import multiprocessing
except ImportError:
    multiprocessing = None
else:       # CPU number if multiprocessing supported
    if os.name == 'posix' and 'SC_NPROCESSORS_CONF' in os.sysconf_names:
        CPU_CNT = os.sysconf('SC_NPROCESSORS_CONF')
    elif 'sched_getaffinity' in os.__all__:
        CPU_CNT = len(os.sched_getaffinity(0))  # pylint: disable=E1101
    else:
        CPU_CNT = os.cpu_count() or 1
finally:    # alias and aftermath
    mp = multiprocessing
    del multiprocessing

# backport compatibility
if sys.version_info[:2] < (3, 5):
    import pathlib2 as pathlib
else:
    import pathlib

# version string
__version__ = '0.5.0'

# macros
__cwd__ = os.getcwd()
__archive__ = os.path.join(__cwd__, 'archive')
__encoding__ = locale.getpreferredencoding()
__pyversion__ = os.environ['F2FORMAT_PYTHONVERSION']


def get_parser():
    parser = argparse.ArgumentParser(prog='f2format',
                                     usage='f2format [options] <python source files and folders...>',
                                     description='Convert f-string to str.format for Python 3 compatibility.')
    parser.add_argument('-V', '--version', action='version', version=__version__)

    archive_group = parser.add_argument_group(title='archive options',
                                              description="duplicate original files in case there's any issue")
    archive_group.add_argument('-n', '--no-archive', action='store_true',
                               help='do not archive original files')
    archive_group.add_argument('-p', '--archive-path', action='store', default=__archive__, metavar='PATH',
                               help='path to archive original files (default is %r)' % __archive__)

    convert_group = parser.add_argument_group(title='convert options',
                                              description='compatibility configuration for lexical analysis')
    convert_group.add_argument('-c', '--encoding', action='store', default=__encoding__, metavar='CODING',
                               help='encoding to open source files (default is %r)' % __encoding__)
    convert_group.add_argument('-v', '--python-version', action='store', metavar='VERSION',
                               default=__pyversion__, choices=['36', '37'],
                               help=('Python version of lexical scanner to analyse source files '
                                     '(default is Python %s)' % __pyversion__))

    parser.add_argument('file', nargs='*', metavar='SOURCE', default=__cwd__,
                        help='python source files and folders to be converted (default is %r)' % __cwd__)

    return parser


def main():
    """Entry point for f2format."""
    parser = get_parser()
    args = parser.parse_args()

    # set up variables
    ARCHIVE = args.archive_path
    archive = (not args.no_archive)
    os.environ['F2FORMAT_ENCODING'] = args.encoding
    os.environ['F2FORMAT_PYTHONVERSION'] = 'py%s' % args.python_version

    # warn if PYTHONVERSION higher than current version
    version = 'py%d%d' % sys.version_info[:2]
    if version < args.python_version:
        warnings.warn(('current Python version is %s; '
                       'some features may not support') % version, FutureWarning)

    def find(root):
        """Recursively find all files under root."""
        flst = list()
        temp = os.listdir(root)
        for file in temp:
            path = os.path.join(root, file)
            if os.path.isdir(path):
                flst.extend(find(path))
            elif os.path.isfile(path):
                flst.append(path)
            elif os.path.islink(path):  # exclude symbolic links
                continue
        yield from flst

    def rename(path):
        stem, ext = os.path.splitext(path)
        name = '%s-%s%s' % (stem, uuid.uuid4(), ext)
        return os.path.join(ARCHIVE, name)

    # make archive directory
    if archive:
        pathlib.Path(ARCHIVE).mkdir(parents=True, exist_ok=True)

    # fetch file list
    filelist = list()
    for path in sys.argv[1:]:
        if os.path.isfile(path):
            if archive:
                dest = rename(path)
                pathlib.Path(dest).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(path, dest)
            filelist.append(path)
        if os.path.isdir(path):
            if archive:
                shutil.copytree(path, rename(path))
            filelist.extend(find(path))

    # check if file is Python source code
    def ispy(file): return (os.path.isfile(file) and (os.path.splitext(file)[1] in ('.py', '.pyw')))
    filelist = set(filter(ispy, filelist))

    # if no file supplied
    if len(filelist) == 0:
        parser.error('argument PATH: no valid source file found')

    # process files
    if mp is None:
        [f2format(filename) for filename in filelist]
    else:
        mp.Pool(processes=CPU_CNT).map(f2format, filelist)


if __name__ == '__main__':
    sys.exit(main())
