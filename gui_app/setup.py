# python3 setup.py bdist_msi
import sys, os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = 'C:/msys64/mingw64/lib/tcl8.6/'
os.environ['TK_LIBRARY'] = 'C:/msys64/mingw64/lib/tk8.6/'

__version__ = "1.0.0"

include_files = ['logo.png']
excludes = [] # ["tkinter"]
packages = ['tkinter', 'ttkthemes', 'PIL', 'queue', 'threading', 'minervaboto', 'os', 'sys']

setup(
    name = 'Renocação Minerva',
    description='Renocação Acervo Minerva',
    version=__version__,
    options = {"build_exe": {
    'packages': packages,
    'include_files': include_files,
    'excludes': excludes,
    'include_msvcr': True,
}},
executables = [Executable("minervaboto-gui.py")]
)
