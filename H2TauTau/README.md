# H->tau tau analysis (CERN/Lyon)

## Installation recipe

```
cmsrel CMSSW_8_0_28_patch1
cd CMSSW_8_0_28_patch1/src 
cmsenv
git cms-init

git remote add colin   git@github.com:cbernet/cmg-cmssw.git
git fetch colin

# configure the sparse checkout, and get the base heppy packages
cp /afs/cern.ch/user/s/steggema/public/sparse-checkout-8025 .git/info/sparse-checkout

# this includes: 
#  - solve conflicts when merging Jan’s branch
#  - MET recipe
#  - MET filter BadGlobalMuonFilter produces a bool  
git co -t colin/heppy_htt8025

# Get MVA MET data file
mkdir RecoMET/METPUSubtraction/data
cd RecoMET/METPUSubtraction/data
wget https://github.com/rfriese/cmssw/raw/MVAMET2_beta_0.6/RecoMET/METPUSubtraction/data/weightfile.root

cd $CMSSW_BASE/src

# now get the CMGTools subsystem from the cmgtools-lite repository
git clone -o cmglite-colin git@github.com:cbernet/cmgtools-lite.git CMGTools
cd CMGTools
git co -t cmglite-colin/828patch1_HTT

scram b -j 8
```

## Running on the grid

The environment must be set in the correct order. *Before doing cmsenv, do:*

```
cd CMGTools/H2TauTau/cfgPython/crab
source ./init.sh
```

This test submission command submits 9 jobs reading the sync miniAOD files. 


```
./heppy_crab.py --AAAconfig=local -s T3_FR_IPNL test/read_sync_file.py
```

The samples that have been produced are stored on `T3_FR_IPNL`. To list these samples, do something like this (change your username and the paths):

```
gfal-ls srm://lyogrid06.in2p3.fr:8446/srm/managerv2?SFN=/dpm/in2p3.fr/home/cms/data/store/user/cbernet/heppyTrees/
>
CMSSW_8_0_28_patch1
```

Finally: 

```
gfal-ls srm://lyogrid06.in2p3.fr:8446/srm/managerv2?SFN=/dpm/in2p3.fr/home/cms/data/store/user/cbernet/heppyTrees/CMSSW_8_0_28_patch1/read_sync_file/HiggsSUSYBB1000/180618_084522/0000
>
heppyOutput_1.tgz
heppyOutput_6.tgz
heppyOutput_7.tgz
heppyOutput_8.tgz
heppyOutput_9.tgz
log
```
