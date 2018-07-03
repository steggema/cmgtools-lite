# H->tau tau analysis, 2017 (CERN/Lyon)

## Installation recipe

If you work in Lyon, do the following to set up your global CMS environment:
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
```

Then follow this recipe to install the analysis software: 

```
export SCRAM_ARCH=slc6_amd64_gcc630
cmsrel CMSSW_9_4_8
cd CMSSW_9_4_8/src 
cmsenv

# add custom CMSSW repo
git remote add colin https://github.com/cbernet/cmg-cmssw.git  -f  -t 94X_HTT

# configure the sparse checkout, and get the base heppy packages
cp /afs/cern.ch/user/c/cmgtools/public/sparse-checkout_94X_heppy .git/info/sparse-checkout
git checkout -t colin/94X_HTT

# get the CMGTools subsystem from the cmgtools-lite repository
git clone -o colin https://github.com/cbernet/cmgtools-lite.git -b 94X_HTT CMGTools

#compile
scram b -j 20
```

## Running our analysis in heppy

Small interactive test: 

```
cd cfgPython/mt
heppy Trash tauMu_2018_cfg.py -N 1000 -f -o production=False
```

## Creation of MINIAOD_CL 

**For now, this step is not necessary for the 2017 analysis**

**Not finalized yet, TODO:**

* provide a vanilla CMSSW release, without CMG tools, for the production of these datasets. the tools and and the instructions will be moved to the sync repository on gitlab
* study the event content in details, and make sure that the necessary products are indeed kept, and that the old ones are dropped.  

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

**The first thing to do is ALWAYS to check that cmsRun runs locally with this configuration before submitting any job:** 

```
cmsRun preprocessor_cfg.py
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

