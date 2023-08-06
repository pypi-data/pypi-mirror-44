import sys
import shutil
import zipfile
from pathlib import Path
from zgh0241.autotest import Autotest
from zgh0241.report import reporter


def extract(zfile, path):
    f = zipfile.ZipFile(zfile, 'r')
    for file in f.namelist():
        f.extract(file, path)


def zgh0241():
    zgh0241_dir = Path(__file__).resolve().parents[0]
    example_dir = zgh0241_dir / 'example' / 'zgh0241_example.zip'
    extract(str(example_dir), Path.cwd())

