import os

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

# 
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
ComponentCreator.useAAA = True


###############
# Options
###############

# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False run locally
production = getHeppyOption('production', False)
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
import CMGTools.H2TauTau.proto.samples.fall17.htt_common as htt_common
from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex
index=ComponentIndex(htt_common)

from CMGTools.H2TauTau.proto.samples.fall17.htt_common import backgrounds_mu, sm_signals, mssm_signals, data_single_muon, sync_list
from CMGTools.H2TauTau.proto.samples.fall17.triggers_tauMu import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.fall17.triggers_tauMu import data_triggers, data_triggerfilters
from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC

mc_list = backgrounds_mu + sm_signals + sync_list + mssm_signals
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

selectedComponents=[]
if production: 
    selectedComponents = data_list if data else backgrounds_mu + sm_signals #+ mssm_signals
else: 
    cache = True
    selectedComponents = index.glob('*BB900*') 
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.fineSplitFactor = 1


events_to_pick = []

###############
# Analyzers 
###############

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, eventSelector, httGenAna, jetAna, triggerAna, recoilCorr, mcWeighter

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

mcWeighter.activate = False

# Just to be sure
if production:
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
    pt1=29, # 2 GeV above IsoMu27 trigger (scale factors start at 29)
    eta1=2.4,
    iso1=0.15,
    looseiso1=9999.,
    pt2=20,
    eta2=2.3,
    iso2=1.5,
    looseiso2=9999.,
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
    addTauMVAInputs=True,
    addVBF=False,
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
