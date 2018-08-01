# python3 setup.py bdist_msi
import sys, os
from cx_Freeze import setup, Executable

__version__ = '1.0.0'

include_files = ['logo.png']
excludes = []
packages = ['queue', 'multiprocessing', 'minervaboto', 'os', 'sys', 'wxPython']

setup(
    name = 'Renovação Minerva',
    description='Renovação Acervo Minerva',
    version=__version__,
    options = {'build_exe': {
    'packages': packages,
    'include_files': include_files,
    'excludes': excludes,
    'include_msvcr': True,
}},
executables = [Executable('minervaboto-gui.pyw')]
)
