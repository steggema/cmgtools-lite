import FWCore.ParameterSet.Config as cms

##____________________________________________________________________________||
process = cms.Process("MERGE")

##____________________________________________________________________________||
process.load("FWCore.MessageLogger.MessageLogger_cfi")

list_of_files = ['root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/4C466283-6BC0-E611-B3AE-001517FB25E4.root',
 'root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/F6E2D0E2-57BF-E611-A90B-A0000420FE80.root',
 'root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/9414A65E-6EBF-E611-9917-02163E012DE6.root',
 'root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/CC6B8919-6EBF-E611-ADDC-001EC94BA3C7.root',
 'root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/9EB65253-62BF-E611-9F58-001E67457DFA.root',
 'root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/14CD7198-67BF-E611-95F9-002590D9D8B8.root',
 'root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/6E606E02-6EBF-E611-B4D4-0CC47AA98B8E.root',
 'root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/5A91079C-69BF-E611-8FE2-0025905A6138.root',
 'root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/BE3452FF-6DBF-E611-BBEB-0CC47A745294.root']

run_events_to_select = [
    [1, [71838,55848]],
]

def vevent_range(run_events):
    verange = cms.untracked.VEventRange()
    for run, events in run_events:
        for event in events: 
            verange.append('{run}:{event}-{run}:{event}'.format(run=run,event=event))
    return verange

print vevent_range(run_events_to_select)

##____________________________________________________________________________||
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        list_of_files
        ),
    # selecting events between event 1 of run 1 and event 10 of run 1. 
    # for a single event, write: '1:5-1:5'
    eventsToProcess = vevent_range(run_events_to_select),
    )

##____________________________________________________________________________||
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('picked_events.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring(
        'keep *'
        )
    )

##____________________________________________________________________________||
process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 50
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))


##____________________________________________________________________________||
process.p = cms.Path()

process.e1 = cms.EndPath(
    process.out
    )

##____________________________________________________________________________||

