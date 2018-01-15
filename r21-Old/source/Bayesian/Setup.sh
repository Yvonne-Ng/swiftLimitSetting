echo "exporting python path"
# python path
export PYTHONPATH=$PWD/inputs/accDictionary:$PWD/plotting/PythonModules:$PYTHONPATH
echo "setting up python to use numpy"
#localSetupSFT --cmtConfig=x86_64-slc6-gcc48-opt pyanalysis/1.4_python2.7
