import os

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor

# 
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
ComponentCreator.useAAA = True

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.TauMuAnalyzer import TauMuAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauMu import H2TauTauTreeProducerTauMu
from CMGTools.H2TauTau.proto.analyzers.TauDecayModeWeighter import TauDecayModeWeighter
from CMGTools.H2TauTau.proto.analyzers.TauFakeRateWeighter import TauFakeRateWeighter
from CMGTools.H2TauTau.proto.analyzers.MuTauFakeReweighter import MuTauFakeReweighter
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.TauP4Scaler import TauP4Scaler
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer import SVfitProducer
from CMGTools.H2TauTau.proto.analyzers.FileCleaner import FileCleaner
from CMGTools.H2TauTau.proto.analyzers.TauIsolationCalculator import TauIsolationCalculator
from CMGTools.H2TauTau.proto.analyzers.MuonIsolationCalculator import MuonIsolationCalculator
from CMGTools.H2TauTau.proto.analyzers.MT2Analyzer import MT2Analyzer
from CMGTools.H2TauTau.proto.analyzers.TauIDWeighter import TauIDWeighter
from CMGTools.H2TauTau.proto.analyzers.METFilter import METFilter


from CMGTools.RootTools.utils.splitFactor import splitFactor

import  CMGTools.H2TauTau.proto.samples.summer16.htt_common as htt_common
from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex
compindex = ComponentIndex(htt_common)

# from CMGTools.H2TauTau.proto.samples.summer16.htt_common import backgrounds_mu, sm_signals, mssm_signals, data_single_muon, sync_list

from CMGTools.H2TauTau.proto.samples.summer16.triggers_tauMu import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.summer16.triggers_tauMu import data_triggers, data_triggerfilters

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, puFileData, puFileMC, eventSelector, httGenAna, jetAna, triggerAna, recoilCorr


# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production', False)
pick_events = getHeppyOption('pick_events', False)
syncntuple = getHeppyOption('syncntuple', True)
cmssw = getHeppyOption('cmssw', True)
cmssw_reuse = getHeppyOption('cmssw_reuse', False)
computeSVfit = getHeppyOption('computeSVfit', False)
data = getHeppyOption('data', False)
tes_string = getHeppyOption('tes_string', '') # '_tesup' '_tesdown'
reapplyJEC = getHeppyOption('reapplyJEC', False)
calibrateTaus = getHeppyOption('calibrateTaus', False) # done in taumuanalyzer because this way sucks.
correct_recoil = getHeppyOption('correct_recoil', True)

# For specific studies
add_iso_info = getHeppyOption('add_iso_info', False)
add_tau_fr_info = getHeppyOption('add_tau_fr_info', False)

if (not cmssw) or production:
    cmssw_reuse = False

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

# Define mu-tau specific modules

#TODO risk to apply to leg1 ? only for leg2 ?
tauP4Scaler = cfg.Analyzer(
    class_object=TauP4Scaler,
    name='TauP4Scaler',
)

tauMuAna = cfg.Analyzer(
    TauMuAnalyzer,
    name='TauMuAnalyzer',
    pt1=23.,
    eta1=2.1,
    iso1=0.15,
    looseiso1=9999.,
    pt2=30.,
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
tauMuMT2Ana = cfg.Analyzer(
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
    disable=False,
)


muonWeighter = cfg.Analyzer(
    LeptonWeighter,
    name='LeptonWeighter_mu',
    scaleFactorFiles={
        'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'm_trgOR4_binned'),
        'iso':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'm_iso_binned'),
        'id':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'm_id'),
        'tracking':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'm_trk'),
        #'trigger':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'm_trgIsoMu24_desy'),
        #'idiso':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'm_idiso0p15_desy'),
        #'tracking':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'm_trk'),
    },
    dataEffFiles={
        #'idiso':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/Muon_IdIso0p20_eff.root', 'm_idiso0p20_desy'),
        #'tracking':('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root', 'm_trk'),
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
    addMoreJetInfo=add_tau_fr_info
)

syncTreeProducer = cfg.Analyzer(
    H2TauTauTreeProducerTauMu,
    name='H2TauTauSyncTreeProducerTauMu',
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
    l1type='muon',
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


tauIDWeighter = cfg.Analyzer(
    TauIDWeighter,
    name='TauIDWeighter',
    legs=['leg2'],
    channel = 'mt',
    ele_WP = 1,
    mu_WP = 4,
    tau_WP = 4,
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
    name='FileCleaner',
    savepreproc = True if cmssw_reuse else False
)


###################################################
###                  SEQUENCE                   ###
###################################################
sequence = commonSequence
if calibrateTaus:
    sequence.insert(sequence.index(httGenAna), tauP4Scaler)
sequence.insert(sequence.index(httGenAna)+1, tauMuAna) # sequence.insert(sequence.index(httGenAna), tauTauAna) initially
sequence.append(tauDecayModeWeighter)
sequence.append(tauFakeRateWeighter) # summer 2013 ??
#sequence.append(muTauFakeWeighter) # included in TauIDWeighter
sequence.append(tauWeighter)
sequence.append(muonWeighter)
if syncntuple:
    sequence.append(tauIDWeighter)

sequence.append(tauMuMT2Ana)
sequence.append(metFilter)

#TODO insert if dosusy part from ttana

if computeSVfit:
    sequence.insert(sequence.index(muonWeighter), svfitProducer)

if add_iso_info:
    sequence.insert(sequence.index(treeProducer), muonIsoCalc)
    sequence.insert(sequence.index(treeProducer), tauIsoCalc)

sequence.append(treeProducer)

if syncntuple:
    sequence.append(syncTreeProducer)

###################################################

# Minimal list of samples
samples = compindex.glob('DYJetsToLL_M50*') # backgrounds_mu + sm_signals + sync_list + mssm_signals

# split_factor = 1e4
split_factor = 5e5 

if computeSVfit:
    split_factor = 5e3

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.puFileData = puFileData
    sample.puFileMC = puFileMC

data_list = compindex.glob('data_single_muon')

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)


# Samples to be processed

# selectedComponents = samples # data_list if data else backgrounds_mu + sm_signals #+ mssm_signals
selectedComponents = compindex.glob('DYJetsToLL_M50_LO_ext')
# selectedComponents[0].splitFactor=1

if pick_events:
    eventSelector.toSelect = [71838,55848]
    sequence.insert(0, eventSelector)


#TODO seems OK but compare to tautaucfg : changes to do here ?
if not cmssw:
    module = [s for s in sequence if s.name == 'MCWeighter'][0]
    sequence.remove(module)

# selectedComponents = [s for s in selectedComponents if s.name=='DYJetsToLL_M50_LO' or ('W' in s.name and 'Jet' in s.name)]

# Batch or local
if not production:
    cache = True
    # selectedComponents = [selectedComponents[-1]] if data else sync_list
    selectedComponents = [selectedComponents[-1]]
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
        comp.files = comp.files[:5]

preprocessor = None
if cmssw:
    if cmssw_reuse and all([os.path.isfile('preprocessed_files/'+comp.name+'/cmsswPreProcessing.root') for comp in selectedComponents]):
        print "Using Preprocessed files! Make sure you don't need to re-run preprocessor!"
        for comp in selectedComponents:
            comp.files = ['preprocessed_files/'+comp.name+'/cmsswPreProcessing.root']
    else:
        #sequence.append(fileCleaner)
        fname = "$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_mutau_data_cfg.py" if data else "$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_mutau{tes_string}_cfg.py".format(tes_string=tes_string)
        preprocessor = CmsswPreprocessor(fname, addOrigAsSecondary=False)
        #selectedComponents[0].files = ['2018-05-22-02/HiggsSUSYBB1000/cmsswPreProcessing.root']

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

hack_evt_sel = False

if hack_evt_sel:
    #import pdb; pdb.set_trace()
    #from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
    #mycreator = ComponentCreator()
    #HiggsSUSYBB1000_picked = mycreator.makeMCComponent(
    #"HiggsSUSYBB1000_picked", "/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 1.0)
    
    selectedComponents = [selectedComponents[0]]
    selectedComponents[0].files = ['/afs/cern.ch/user/l/ltortero/H2TauTau_weights_debug/picked_events.root']


config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    preprocessor=preprocessor,
                    events_class=Events
                    )

printComps(config.components, True)
