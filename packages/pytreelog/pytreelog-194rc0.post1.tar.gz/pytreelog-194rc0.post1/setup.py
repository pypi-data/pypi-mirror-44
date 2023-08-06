#!/usr/bin/env python

from setuptools import setup, find_packages
import os, shutil
from os import path

#import traceback
#import logging

#try:
#    whatever()
#except Exception as e:
#    logging.error(traceback.format_exc())
    # Logs the error appropriately.
    

#this_dir = path.abspath(path.dirname(__file__))
#print( 'this_directory={}'.format(this_dir)) 
#with open(path.join(this_dir, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()


# To allow the README.md to be collected by setup(), we can put
# README.md in pytreelog-pkg/pytreelog/ folder. But a better 
# approach is below, in which the README.md remains in the 
# package root folder so a git can use it directly for doc:

# Copy README.md from pytreelog-pkg/ to pytreelog-pkg/pytreelog/
# for setup() to pick it up, which also requires:
# -- include_package_data=True in setup() and
# -- MENIFEST.in (content: include pytreelog/README.md )
#
print( "###### Entering setup.py ######" )
setup_path = os.path.split(os.path.realpath( __file__ ))[0]
README_from = os.path.join( setup_path,'README.md')
README_to   = os.path.join( setup_path,'pytreelog','README.md')
print( '\nCopy README.md from \n"{}" \nto \n"{}" \nfor setuptools.setup()\n'.format( README_from, README_to ) )
shutil.copyfile( README_from, README_to )

with open(README_from, encoding='utf-8') as f:
    long_description = f.read()

try:
  setup(name='pytreelog',
        version='194c.post1',
        description='Tree-like logging util for python',
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='runsun',
        author_email='runsun@gmail.com',
        url='https://gitlab.com/runsun/pytreelog',
        packages=find_packages(),
        py_modules = ["pytreelog"],
        include_package_data=True, # Need this to include README.md in the pacakge
        classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
         ]
       )
finally:
  print( '\nDeleting "{}"\n'.format( README_to ) )
  os.remove( README_to )
  print( "###### Leaving setup.py ######" )

# Keep setup doc here for future ref:

__setup_doc__= r"""
---------------------------------------------------
### 0) File structure:

pytreelog-pkg/
|- __init__.py
|- README.md
|- MANIFEST.in
|- setup.py
|- pytreelog/ 
    |- pytreelog.py

Where MANIFEST.in contains:

include pytreelog/README.md

--------------------------------------------------
### 1) Run setup:

```...\pytreelog-pkg > py setup.py sdist bdist_wheel```
 
This creates 3 folders under `pytreelog-pkg/`:

```
   build/
   dist/ 
   pytreelog_runsun.egg-info/ 
```
 
---------------------------------------------------
### 2) Local pip install: Test a pip insall locally:

```...\pytreelog-pkg > pip install dist/pytreelog_runsun-201949.post1-py3-none-any.whl```
 
This creates 2 folders under `... python37/Lib/site-packages/`:

```
   pytreelog_runsun-20190408.post2.dist-info/
   pytreelog/
     |- pytreelog.py
     |- README.md
```

---------------------------------------------------
3) Test:
```
C:\> py
Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from pytreelog import pytreelog as pt
>>> pt.test()
--- Loading "C:\python37\lib\site-packages\pytreelog\README.md" for doctest:
--- Tests done.
>>>
```

---------------------------------------------------
### 4) If all goes well, uploda it to `test.pypi.org`:

```
...\pytreelog-pkg> py -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
 
---------------------------------------------------
### 5) Then pip install from test.pypi.org:

It's better to uninstall pytreelog from python first :

```
pip uninstall pytreelog-runsun
```
Then install from test.pypi.org

```
...\pytreelog-pkg> pip install -i https://test.pypi.org/simple/ pytreelog-runsun --upgrade 
```

---------------------------------------------------
### 6) if all go well, repeat 4),5) but use pypi.prg instead 


pip install git+https://gitlab.com/runsun/pytreelog.git

ref: 

# pit install from git repo:

pip install git+https://github.com/myuser/foo.git
pip install git+https://github.com/myuser/foo.git@v123
pip install git+https://github.com/myuser/foo.git@newbranch
 
https://stackoverflow.com/questions/8247605/configuring-so-that-pip-install-can-work-from-github
https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support

"""
