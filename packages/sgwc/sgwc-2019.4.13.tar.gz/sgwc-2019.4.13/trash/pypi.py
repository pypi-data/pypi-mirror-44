from os import system, chdir
from shutil import rmtree
from pathlib import Path
from time import sleep

command1 = 'python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*'
command2 = 'python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*'
path1 = Path('../build')
path2 = Path('../dist')
path3 = Path('../sgwc.egg-info')
path_set = [path1, path2, path3]

for p in path_set:
    if p.exists():
        rmtree(p)

chdir('../')
system('python setup.py sdist bdist_wheel')
