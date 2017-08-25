#!bin/bash

rm -rf build/
mkdir build/
cd build/
cmake ../source
cp ../make.sh .
source make.sh

