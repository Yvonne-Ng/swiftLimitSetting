#first setup the appropriate ATLAS release
#asetup 20.1.X.Y-VAL,rel_N,AtlasDerivation,gcc48,here --nightliesarea=/afs/cern.ch/atlas/software/builds/nightlies/ 

echo -e "\ncheck out packages"
cmt co PhysicsAnalysis/DerivationFramework/DerivationFrameworkCore
cmt co PhysicsAnalysis/DerivationFramework/DerivationFrameworkExotics
cmt co PhysicsAnalysis/DerivationFramework/DerivationFrameworkJetEtMiss

echo -e "\nsetup and compile"
cd $TestArea
setupWorkArea.py
cd WorkArea/cmt
cmt bro cmt config
cmt bro gmake
cd $TestArea/WorkArea/run

echo -e "\ndone"
