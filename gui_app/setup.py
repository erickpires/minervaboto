# python3 setup.py bdist_msi
import sys, os
from cx_Freeze import setup, Executable

__version__ = '1.0.0'

include_files = ['logo.png']
excludes = []
packages = ['wxPython', 'queue', 'threading', 'minervaboto', 'os', 'sys']

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
executables = [Executable('minervaboto-gui.py')]
)
