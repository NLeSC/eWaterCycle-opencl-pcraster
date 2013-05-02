#!/usr/bin/env bash

OLD_PWD=`pwd`
SCRIPT_DIR=$(cd `dirname $0` && pwd)

#set environment, changes dir as a side effect
unset OBJECTS
export DEVELOPMENT_ROOT=$HOME/Development
export PROJECTS=$DEVELOPMENT_ROOT/projects
export PCRTEAM_EXTERN_ROOT=$HOME/pcrteam_extern
source $PROJECTS/devenv/configuration/profiles/Utils.sh
source $PROJECTS/pcraster/environment/configuration/PCRaster-master

cd $OLD_PWD

$SCRIPT_DIR/make_dist_build_package.sh $1
