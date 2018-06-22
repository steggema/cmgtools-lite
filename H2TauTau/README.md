# H->tau tau analysis (CERN/Lyon)

## Installation recipe

If you work in Lyon, do the following to set up your global CMS environment:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
```

Then follow this recipe to install the analysis software: 

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

In the new computing model, we do not run the preprocessor anymore in heppy. 
Instead, we perform some of the tasks that were done by the preprocessor with cmsRun directly, and produce MINIAOD_CL events. These events are later on read with heppy. They are common to all analysis channels. 

Set up your environment for GRID usage, and go to the `crab` directory: 

```
cd $CMSSW_BASE/src/CMGTools/H2TauTau
source ./init.sh
cd crab 
```

Set up a link to the cmsRun configuration file for the production of MINIAOD_CL events: 

```
ln -s ../python/h2TauTauMiniAOD_any_cfg.py preprocessor_cfg.py
```

Initialize your proxy:

```
voms-proxy-init -voms cms
```

To submit production tasks to the GRID, we use `crabSubmit.py`. Read the documentation of this script carefully:

```
crabSubmit.py -h 
```

Check available samples matching a given pattern: 

```
listhttsamples.py '*BB*'
>
[HiggsSUSYBB450:/SUSYGluGluToBBHToTauTau_M-450_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM,
 HiggsSUSYBB400:/SUSYGluGluToBBHToTauTau_M-400_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM,
... 
```

Let's narrow the choice to the sync sample: 

```
listhttsamples.py HiggsSUSYBB1000
[HiggsSUSYBB1000:/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM]
```

Create a CRAB task for this sample (always use the `-n` option until you are sure about what you are going to submit):

```
crabSubmit.py HiggsSUSYBB1000 -e 10000 -n 
Task:   /SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM
        files/job = 1
        n jobs    = 9
```

If you're happy with the result (1 task with 9 jobs, each job reading 1 input file), remove the `-n` option to submit: 

```
crabSubmit.py HiggsSUSYBB1000 -e 10000  
```

After submission, use 

```
crab status 
```

To get the links to the dashboard, where you'll be able to follow your jobs.

