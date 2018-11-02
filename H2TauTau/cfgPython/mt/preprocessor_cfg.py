from CMGTools.H2TauTau.preprocessor.h2TauTauMiniAOD_mutau_cfg import * 

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
DYJetsToLL_M50_LO_ext =  kreator.makeMCComponent("DYJetsToLL_M50_LO_ext", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM", "CMS", ".*root", 2008.*3)
process.source.fileNames = DYJetsToLL_M50_LO_ext.files

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(20000)
)

# logging, verbosity, etc
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(True)
)

 
