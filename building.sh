#!bin/bash

rm -rf build/
mkdir build/
cd build/
cmake ../source
make 
make install DESTDIR=../install

