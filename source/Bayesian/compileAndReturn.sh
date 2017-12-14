cd ../../build
cmake ../source
make
make install DESTDIR=../install
source ../install/InstallArea/${AnalysisBase_PLATFORM}/setup.sh
cd ../source/Bayesian