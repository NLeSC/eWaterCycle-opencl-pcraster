#!/usr/bin/env python

from __future__ import print_function
import subprocess
import os
import sys
import time
import urllib
import tarfile
import shutil
import subprocess


scriptdir = os.path.dirname(os.path.abspath(__file__))
pcraster_dir = os.path.dirname(scriptdir)

distdir = os.path.join(pcraster_dir, 'pcraster-custom')

#move old dist dir if needed
if os.path.exists(distdir):
    number = 0
    while os.path.exists(distdir + ".old." + str(number)):
        number += 1
        
    target = distdir + ".old." + str(number) 
        
    os.rename(distdir, target)

#remove old build tmp if needed
build_tmp = os.path.join(pcraster_dir, 'dist_tmp')
if os.path.exists(build_tmp):
    shutil.rmtree(build_tmp)

os.mkdir(build_tmp)

#call bash script to make pcraster package.
bash_script = os.path.join(scriptdir, 'make_dist_set_environment.sh')

return_code = subprocess.call(bash_script + " " + distdir, shell=True, cwd=build_tmp)

sys.exit(0)

if (return_code != 0):
    sys.exit(return_code)

#copy native libraries
dist_lib = os.path.join(distdir, 'lib')
pcraster_lib = os.path.join(pcraster_dir, 'lib')

shutil.rmtree(pcraster_lib);
shutil.copytree(dist_lib, pcraster_lib)

#copy native so files from python path
dist_python_pcraster = os.path.join(distdir, 'python', 'pcraster')
pcraster_python_pcraster = os.path.join(pcraster_dir, 'src', 'pcraster')

for file in {'_pcraster.so', '_pcraster_modflow.so', 'moc/_pcraster_moc.so', 'mldd/_pcraster_mldd.so' }:
    shutil.copy(os.path.join(dist_python_pcraster, file), os.path.join(pcraster_python_pcraster, file))

#done
print('done')

