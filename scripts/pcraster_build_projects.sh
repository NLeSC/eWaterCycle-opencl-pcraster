#!/bin/bash

unset OBJECTS

export DEVELOPMENT_ROOT=$HOME/Development
export PROJECTS=$DEVELOPMENT_ROOT/projects
export PCRTEAM_EXTERN_ROOT=$HOME/pcrteam_extern

source $PROJECTS/devenv/configuration/profiles/Utils.sh

source $PROJECTS/pcraster/environment/configuration/PCRaster-master

/home/niels/Development/projects/pcraster/environment/scripts/make_pcraster_package_linux.sh
