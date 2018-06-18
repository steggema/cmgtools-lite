import os

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.TauEleAnalyzer import TauEleAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauEle import H2TauTauTreeProducerTauEle
from CMGTools.H2TauTau.proto.analyzers.DYLLReweighterTauEle import DYLLReweighterTauEle
from CMGTools.H2TauTau.proto.analyzers.TauDecayModeWeighter import TauDecayModeWeighter
from CMGTools.H2TauTau.proto.analyzers.TauFakeRateWeighter import TauFakeRateWeighter
# EleTauFakeReweighter ?
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.TauP4Scaler import TauP4Scaler
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer import SVfitProducer
from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner
from CMGTools.H2TauTau.proto.analyzers.TauIsolationCalculator import TauIsolationCalculator
from CMGTools.H2TauTau.proto.analyzers.LeptonIsolationCalculator import LeptonIsolationCalculator
from CMGTools.H2TauTau.proto.analyzers.MT2Analyzer import MT2Analyzer
from CMGTools.H2TauTau.proto.analyzers.TauIDWeighter import TauIDWeighter
from CMGTools.H2TauTau.proto.analyzers.METFilter import METFilter


from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.summer16.htt_common import backgrounds_ele, sm_signals, mssm_signals, data_single_electron, sync_list
from CMGTools.H2TauTau.proto.samples.summer16.triggers_tauEle import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.summer16.triggers_tauEle import data_triggers, data_triggerfilters


# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, puFileData, puFileMC, eventSelector, httGenAna, jetAna, triggerAna, recoilCorr

# e-tau specific configuration settings


# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production', False)
pick_events = getHeppyOption('pick_events', False)
syncntuple = getHeppyOption('syncntuple', True)
cmssw = getHeppyOption('cmssw', True)
cmssw_reuse = getHeppyOption('cmssw_reuse', True)
doSUSY = getHeppyOption('susy', False)
computeSVfit = getHeppyOption('computeSVfit', False)
data = getHeppyOption('data', False)
tes_string = getHeppyOption('tes_string', '') # '_tesup' '_tesdown'
reapplyJEC = getHeppyOption('reapplyJEC', False)
calibrateTaus = getHeppyOption('calibrateTaus', False) # done in taueleanalyzer because this way sucks.
scaleTaus = getHeppyOption('scaleTaus', False)
correct_recoil = getHeppyOption('correct_recoil', True)

# For specific studies
add_iso_info = getHeppyOption('add_iso_info', False)
add_tau_fr_info = getHeppyOption('add_tau_fr_info', False)

shift = None # ??

if doSUSY:
    cmssw = False

if (not cmssw) or production:
    cmssw_reuse = False

tes_up = False
tes_scale = 1.0
if tes_up:
    scaleTaus = True
    tes_scale = 1.03

# Just to be sure
if production:
    # syncntuple = False
    pick_events = False

if reapplyJEC:
    if cmssw:
        jetAna.jetCol = 'patJetsReapplyJEC'
        httGenAna.jetCol = 'patJetsReapplyJEC'
    else:
        jetAna.recalibrateJets = True

if correct_recoil:
    recoilCorr.apply = True

if not data:
    triggerAna.requireTrigger = False

# Define e-tau specific modules

#TODO risk to apply to leg1 ? only for leg2 ?
tauP4Scaler = cfg.Analyzer(
    class_object=TauP4Scaler,
    name='TauP4Scaler',
)

tauEleAna = cfg.Analyzer(
    TauEleAnalyzer,
    name='TauEleAnalyzer',
    pt1=26,
    eta1=2.1,
    iso1=0.1,
    looseiso1=9999.,
    pt2=30,
    eta2=2.3,
    iso2=1., #1.5
    looseiso2=9999.,
    m_min=10,
    m_max=99999,
    dR_min=0.5,
    from_single_objects=False if cmssw else True,
    ignoreTriggerMatch=True, # best dilepton doesn't need trigger match
    verbose=False,
    tauEnergyScale=True,
)

#TODO changes to do with respect to the tauTauMT2Ana ?
eleMuMT2Ana = cfg.Analyzer(
    MT2Analyzer, name='MT2Analyzer',
    metCollection="slimmedMETs",
    doOnlyDefault=False,
    jetPt=40.,
    collectionPostFix="",
    verbose=True
)

tauDecayModeWeighter = cfg.Analyzer(
    TauDecayModeWeighter,
    name='TauDecayModeWeighter',
    legs=['leg2']
)

dyLLReweighterTauEle = cfg.Analyzer(
    DYLLReweighterTauEle,
    name='DYLLReweighterTauEle',
    # 2012
    W1p0PB=1.,  # 1.37, # weight for 1 prong 0 Pi Barrel
    W1p0PE=1.,  # 1.11,
    W1p1PB=1.,  # 2.18,
    W1p1PE=1.,  # 0.47,
    verbose=False
)

tauFakeRateWeighter = cfg.Analyzer(
    TauFakeRateWeighter,
    name='TauFakeRateWeighter'
)

tauWeighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_tau',
    scaleFactorFiles = {},
    lepton='leg2',
    disable=True,
)

#TODO weights to be modified ?
eleWeighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_ele',
    scaleFactorFiles={
        'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'e_trg_binned'),
        'iso':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'e_iso_binned'),
        'id':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'e_id'),
        'tracking':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'e_trk'),
        # 'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v3.root', 'trgIsoMu22_desy'),
        #'idiso':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v5.root', 'e_idiso0p10_desy'),
        #'tracking':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v5.root', 'e_trk'),
    },
    dataEffFiles={
        #'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v5.root', 'e_trgEle25eta2p1WPTight_desy'),
    },
    lepton='leg1',
    disable=False
)

treeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauEle,
    name='H2TauTauTreeProducerTauEle',
    addIsoInfo=add_iso_info,
    addTauTrackInfo=add_tau_fr_info,
    addMoreJetInfo=add_tau_fr_info
)

syncTreeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauEle,
    name='H2TauTauSyncTreeProducerTauEle',
    varStyle='sync',
    skimFunction=' and '.join(['event.'+met_filter for met_filter in ['Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter', 'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_goodVertices', 'Flag_eeBadScFilter', 'Flag_globalTightHalo2016Filter', 'passBadMuonFilter', 'passBadChargedHadronFilter', 'passBadGlobalMuonFilter', 'passcloneGlobalMuonFilter']])#
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
    l1type='ele',
    l2type='tau'
)

metFilter = cfg.Analyzer(
    METFilter,
    name='METFilter',
    processName='PAT',
    triggers=[
        'Flag_HBHENoiseFilter', 
        'Flag_HBHENoiseIsoFilter', 
        'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_goodVertices',
        'Flag_eeBadScFilter',
        'Flag_globalTightHalo2016Filter'
    ]
)

# seems like leg1 == ele and leg2 == tauh ?
tauIDWeighter = cfg.Analyzer(
    TauIDWeighter,
    name='TauIDWeighter',
    legs=['leg2'],
    channel = 'et',
    ele_WP = 4,
    mu_WP = 2,
    tau_WP = 4,
)

tauIsoCalc = cfg.Analyzer(
    TauIsolationCalculator,
    name='TauIsolationCalculator',
    getter=lambda event: [event.leg2]
)

electronIsoCalc = cfg.Analyzer(
    LeptonIsolationCalculator,
    name='ElectronIsolationCalculator',
    lepton='electron',
    getter=lambda event: [event.leg1]
)

fileCleaner = cfg.Analyzer(
    FileCleaner,
    name='FileCleaner',
    savepreproc = True if cmssw_reuse else False
)

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = commonSequence
if calibrateTaus:
    sequence.insert(sequence.index(httGenAna), tauP4Scaler)
sequence.insert(sequence.index(httGenAna)+1, tauEleAna)
sequence.append(tauDecayModeWeighter)
#sequence.append(tauFakeRateWeighter) # summer 2013 ??
sequence.append(tauWeighter)
sequence.append(eleWeighter)
#sequence.insert(sequence.index(tauEleAna) + 1, dyLLReweighterTauEle)
if syncntuple:
    sequence.append(tauIDWeighter)
sequence.append(eleMuMT2Ana)
sequence.append(metFilter)

#TODO insert if dosusy part from ttana

if computeSVfit:
    sequence.insert(sequence.index(eleWeighter), svfitProducer)

if add_iso_info:
    sequence.insert(sequence.index(treeProducer), electronIsoCalc)
    sequence.insert(sequence.index(treeProducer), tauIsoCalc)

sequence.append(treeProducer)

if syncntuple:
    sequence.append(syncTreeProducer)

###################################################

# Minimal list of samples
samples = [sync_list[0]] # backgrounds_ele + sm_signals + mssm_signals + sync_list

split_factor = 1e4

if computeSVfit:
    split_factor = 5e3

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.puFileData = puFileData
    sample.puFileMC = puFileMC

data_list = data_single_electron

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)


# Samples to be processed

selectedComponents = samples # data_list if data else backgrounds_mu + sm_signals #+ mssm_signals
#selectedComponents = samples + data_list

if pick_events:
    eventSelector.toSelect = [1310750]
    sequence.insert(0, eventSelector)


#TODO seems OK but compare to tautaucfg : changes to do here ?
if not cmssw:
    module = [s for s in sequence if s.name == 'MCWeighter'][0]
    sequence.remove(module)

# Batch or local
if not production:
    cache = True
    # selectedComponents = [selectedComponents[-1]] if data else sync_list
    # comp = my_connect.mc_dict['HiggsGGH125']
    # comp = sync_list[0]
    #selectedComponents = sync_list
    selectedComponents = [selectedComponents[-1]]
    for comp in selectedComponents:
        comp.splitFactor = 1 # 100
        comp.fineSplitFactor = 1
        comp.files = [comp.files[0]]
#    comp.files = comp.files[:1]

preprocessor = None
if cmssw:
    if cmssw_reuse and all([os.path.isfile('preprocessed_files/'+comp.name+'/cmsswPreProcessing.root') for comp in selectedComponents]):
        print "Using Preprocessed files! Make sure you don't need to re-run preprocessor!"
        for comp in selectedComponents:
            comp.files = ['preprocessed_files/'+comp.name+'/cmsswPreProcessing.root']
    else:
        sequence.append(fileCleaner)
        preprocessor = CmsswPreprocessor("$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_etau_cfg.py", addOrigAsSecondary=False)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    preprocessor=preprocessor,
                    events_class=Events
                    )

printComps(config.components, True)
