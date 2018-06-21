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

## Running our analysis in heppy

to be written

## Creation of MINIAOD_CL 

to be written