#!/bin/bash

POCL_SCRIPT_DIR=$(cd `dirname $0` && pwd)
POCL_DIST_BUILD_DIR=$POCL_SCRIPT_DIR/../new_dist

echo building pcraster distribution in $POCL_DIST_DIR

rm -rf $POCL_DIST_BUILD_DIR
mkdir $POCL_DIST_BUILD_DIR
cd $POCL_DIST_BUILD_DIR

unset OBJECTS

export DEVELOPMENT_ROOT=$HOME/Development
export PROJECTS=$DEVELOPMENT_ROOT/projects
export PCRTEAM_EXTERN_ROOT=$HOME/pcrteam_extern

source $PROJECTS/devenv/configuration/profiles/Utils.sh

source $PROJECTS/pcraster/environment/configuration/PCRaster-master

cd $POCL_DIST_BUILD_DIR

#use standard pcraster package script
make_pcraster_package_linux.sh

POCL_BASE_NAME="pcraster-${PCRTEAM_PLATFORM##*/}-`date +%Y%m%d`"

cd $POCL_DIST_BUILD_DIR
tar zxvf $POCL_BASE_NAME.tar.gz
mv $POCL_BASE_NAME dist
