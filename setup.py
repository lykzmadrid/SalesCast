import cx_Freeze, sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py", base=base, targetName="NAME_OF_EXE")]

cx_Freeze.setup(
    name="main",
    version="1.0",
    description="DESCRIBE YOUR PROGRAM",
    executables=executables
)