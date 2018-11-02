import os

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

# 
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
ComponentCreator.useAAA = True

import logging
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

###############
# Options
###############

# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False run locally
test = getHeppyOption('test', True)
syncntuple = getHeppyOption('syncntuple', False)
data = getHeppyOption('data', False)
tes_string = getHeppyOption('tes_string', '') # '_tesup' '_tesdown'
reapplyJEC = getHeppyOption('reapplyJEC', True)
correct_recoil = getHeppyOption('correct_recoil', False) # Not yet for 2017 analysis
# For specific studies
add_iso_info = getHeppyOption('add_iso_info', False)
add_tau_fr_info = getHeppyOption('add_tau_fr_info', False)

###############
# global tags
###############

gt_mc = 'Fall17_17Nov2017_V6_MC'
gt_data = 'Fall17_17Nov2017{}_V6_DATA'

###############
# Components
###############

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex
import CMGTools.H2TauTau.proto.samples.fall17.higgs as higgs
index=ComponentIndex(higgs)

from CMGTools.H2TauTau.proto.samples.fall17.data import data_single_muon
from CMGTools.H2TauTau.proto.samples.fall17.higgs_susy import mssm_signals
from CMGTools.H2TauTau.proto.samples.fall17.higgs import sync_list
from CMGTools.H2TauTau.proto.samples.fall17.backgrounds import backgrounds
from CMGTools.H2TauTau.proto.samples.fall17.triggers_tauMu import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.fall17.triggers_tauMu import data_triggers, data_triggerfilters
from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC

mc_list = backgrounds + sync_list + mssm_signals
data_list = data_single_muon

n_events_per_job = 1e5

for sample in mc_list:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, n_events_per_job)
    sample.puFileData = puFileData
    sample.puFileMC = puFileMC

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, n_events_per_job)
    sample.dataGT = gt_data.format(sample.name[sample.name.find('2017')+4])

selectedComponents = data_list if data else backgrounds + mssm_signals


if test:
    cache = True
    comp = index.glob('HiggsVBF125')[0]
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [comp]
    # comp.files = ['test.root']

events_to_pick = []

###############
# Analyzers 
###############

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, eventSelector, httGenAna, jetAna, triggerAna, recoilCorr

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.TauMuAnalyzer import TauMuAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauMu import H2TauTauTreeProducerTauMu
from CMGTools.H2TauTau.proto.analyzers.TauDecayModeWeighter import TauDecayModeWeighter
from CMGTools.H2TauTau.proto.analyzers.TauFakeRateWeighter import TauFakeRateWeighter
from CMGTools.H2TauTau.proto.analyzers.MuTauFakeReweighter import MuTauFakeReweighter
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer import SVfitProducer
from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner
from CMGTools.H2TauTau.proto.analyzers.TauIsolationCalculator import TauIsolationCalculator
from CMGTools.H2TauTau.proto.analyzers.MuonIsolationCalculator import MuonIsolationCalculator


# Just to be sure
if not test:
    syncntuple = False
    pick_events = False

if reapplyJEC:
    jetAna.recalibrateJets = True
    jetAna.mcGT = gt_mc
    jetAna.dataGT = gt_data

# todo : reuse the same name as in mini aod when doing this in cmssw
#    if cmssw:
#        jetAna.jetCol = 'patJetsReapplyJEC'
#        httGenAna.jetCol = 'patJetsReapplyJEC'

if correct_recoil:
    recoilCorr.apply = True

if not data:
    triggerAna.requireTrigger = False

# Define mu-tau specific modules

tauMuAna = cfg.Analyzer(
    TauMuAnalyzer,
    name='TauMuAnalyzer',
    pt1=21,
    eta1=2.1,
    iso1=None, # no iso cut for sync
    pt2=20,
    eta2=2.3,
    iso2=1.5,
    m_min=10,
    m_max=99999,
    dR_min=0.5,
    from_single_objects=True,
    ignoreTriggerMatch=True, # best dilepton doesn't need trigger match
    verbose=False
)

tauDecayModeWeighter = cfg.Analyzer(
    TauDecayModeWeighter,
    name='TauDecayModeWeighter',
    legs=['leg2']
)

muTauFakeWeighter = cfg.Analyzer(
    MuTauFakeReweighter,
    name='MuTauFakeReweighter',
    wp='tight'
)

tauFakeRateWeighter = cfg.Analyzer(
    TauFakeRateWeighter,
    name='TauFakeRateWeighter'
)

tauWeighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_tau',
    scaleFactorFiles={},
    lepton='leg2',
    disable=True,
)

muonWeighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_mu',
    scaleFactorFiles={
        'id':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/RunBCDEF_SF_ID.json', 'NUM_MediumID_DEN_genTracks'),
        'iso':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/RunBCDEF_SF_ISO.json', 'NUM_TightRelIso_DEN_MediumID'),
        'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/theJSONfile_RunBtoF_Nov17Nov2017.json', 'IsoMu27_PtEtaBins')
    },
    dataEffFiles={
        # 'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_2.root', 'm_trgIsoMu22orTkIsoMu22_desy'),
    },
    lepton='leg1',
    disable=False
)

treeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauMu,
    name='H2TauTauTreeProducerTauMu',
    addIsoInfo=add_iso_info,
    addTauTrackInfo=add_tau_fr_info,
    addMoreJetInfo=add_tau_fr_info,
    addTauMVAInputs=False,
    addVBF=True,
    skimFunction='event.leg1.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=False)<0.15 and event.leg2.tauID("againstMuonLoose3")>0.5 and (event.leg2.tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits") > 0.5 or event.leg2.tauID("byVLooseIsolationMVArun2v1DBoldDMwLT") > 0.5)'
)

syncTreeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauMu,
    name='H2TauTauSyncTreeProducerTauMu',
    varStyle='sync',
    # skimFunction='event.isSignal'
)

svfitProducer = cfg.Analyzer(
    SVfitProducer,
    name='SVfitProducer',
    # integration='VEGAS',
    integration='MarkovChain',
    # verbose=True,
    # order='21', # muon first, tau second
    integrateOverVisPtResponse = True          ,
    visPtResponseFile = os.environ['CMSSW_BASE']+'/src/CMGTools/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root', 
    l1type='muon',
    l2type='tau'
)

tauIsoCalc = cfg.Analyzer(
    TauIsolationCalculator,
    name='TauIsolationCalculator',
    getter=lambda event: [event.leg2]
)

muonIsoCalc = cfg.Analyzer(
    MuonIsolationCalculator,
    name='MuonIsolationCalculator',
    getter=lambda event: [event.leg1]
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner'
)

##################
# Sequence
##################

sequence = commonSequence
sequence.insert(sequence.index(httGenAna), tauMuAna)
# sequence.append(tauDecayModeWeighter) # not measured in 2017
# sequence.append(tauFakeRateWeighter) # empty
sequence.append(muTauFakeWeighter)
# sequence.append(tauWeighter) # empty
sequence.append(muonWeighter)
sequence.append(treeProducer)

if syncntuple:
    sequence.append(syncTreeProducer)

if add_iso_info:
    sequence.insert(sequence.index(treeProducer), muonIsoCalc)
    sequence.insert(sequence.index(treeProducer), tauIsoCalc)

if events_to_pick:
    eventSelector.toSelect = events_to_pick
    sequence.insert(0, eventSelector)


# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )

printComps(config.components, True)

