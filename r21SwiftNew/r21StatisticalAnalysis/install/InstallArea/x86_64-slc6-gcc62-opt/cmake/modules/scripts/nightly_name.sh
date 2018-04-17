#!/bin/bash
#
# Copyright (C) 2002-2017 CERN for the benefit of the ATLAS collaboration
#
# Script constructing a readable "nightly name" for the project being
# built. Either printing the exact tag that the build was made from,
# or a descriptive name of the branch.
#

git describe --exact-match 2> /dev/null || \
    git symbolic-ref HEAD 2> /dev/null | cut -d/ -f3
