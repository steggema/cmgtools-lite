import PhysicsTools.HeppyCore.framework.config as cfg

# import all analysers:
# Heppy analyzers
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
from PhysicsTools.Heppy.analyzers.core.EventSelector import EventSelector
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
# from PhysicsTools.Heppy.analyzers.gen.GeneratorAnalyzer import GeneratorAnalyzer
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer import LHEWeightAnalyzer

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.JetAnalyzer import JetAnalyzer
from CMGTools.H2TauTau.proto.analyzers.METAnalyzer import METAnalyzer
from CMGTools.H2TauTau.proto.analyzers.EmbedWeighter import EmbedWeighter
from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer
from CMGTools.H2TauTau.proto.analyzers.HTTGenMatcher import HTTGenMatcher
from CMGTools.H2TauTau.proto.analyzers.NJetsAnalyzer import NJetsAnalyzer
# from CMGTools.H2TauTau.proto.analyzers.HiggsPtWeighter import HiggsPtWeighter
from CMGTools.H2TauTau.proto.analyzers.VBFAnalyzer import VBFAnalyzer
from CMGTools.H2TauTau.proto.analyzers.RecoilCorrector import RecoilCorrector
from CMGTools.H2TauTau.proto.analyzers.METFilter import METFilter

# TTH analyzers
from CMGTools.TTHAnalysis.analyzers.ttHhistoCounterAnalyzer import ttHhistoCounterAnalyzer
from CMGTools.TTHAnalysis.analyzers.susyParameterScanAnalyzer import susyParameterScanAnalyzer

puFileMC = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/pudistributions_mc_2017_artur_Jul9.root'
puFileData = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/pudistributions_data_2017.root'

# badMuonAnaMoriond2017 = cfg.Analyzer(
#     badMuonAnalyzerMoriond2017, name='badMuonMoriond2017',
#     muons='slimmedMuons',
#     vertices='offlineSlimmedPrimaryVertices',
#     minMuPt=20,
#     selectClones=False,
#     postFix='',
# )

susyCounter = cfg.Analyzer(
    ttHhistoCounterAnalyzer, name="ttHhistoCounterAnalyzer",
    SMS_max_mass=3000,  # maximum mass allowed in the scan
    # SMS_mass_1='genSusyMScan1',  # first scanned mass
    # SMS_mass_2='genSusyMScan2',  # second scanned mass
    SMS_mass_1='genSusyMChargino',  # first scanned mass
    SMS_mass_2='genSusyMNeutralino',  # second scanned mass
    # other mass variables that are expected to change in the tree (e.g., in T1tttt it should be set to ['genSusyMGluino','genSusyMNeutralino'])
    SMS_varying_masses=['genSusyMStau'],
    SMS_regexp_evtGenMass='genSusyM.+',
    bypass_trackMass_check=True  # bypass check that non-scanned masses are the same in all events
)

eventSelector = cfg.Analyzer(
    EventSelector,
    name='EventSelector',
    toSelect=[]
)

lheWeightAna = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
    useLumiInfo=False
)

jsonAna = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

skimAna = cfg.Analyzer(
    SkimAnalyzerCount,
    name='SkimAnalyzerCount'
)


triggerAna = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=True,
    usePrescaled=False
)

vertexAna = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    keepFailingEvents=True,
    verbose=False
)

pileUpAna = cfg.Analyzer(
    PileUpAnalyzer,
    name='PileUpAnalyzer',
    true=True,
    autoPU=False
)

# genAna = GeneratorAnalyzer.defaultConfig

# genAna.savePreFSRParticleIds = [1, 2, 3, 4, 5, 21]

# Save SUSY masses
susyScanAna = cfg.Analyzer(
    susyParameterScanAnalyzer, name="susyParameterScanAnalyzer",
    doLHE=True,
    useLumiInfo=False,
)

httGenAna = cfg.Analyzer(
    HTTGenAnalyzer,
    name='HTTGenAnalyzer',
    jetCol='slimmedJets',
    genPtCut=8.
)

httGenMatcher = cfg.Analyzer(
    HTTGenMatcher,
    name='HTTGenMatcher'
)

jetAna = cfg.Analyzer(
    JetAnalyzer,
    name='JetAnalyzer',
    jetCol='slimmedJets',
    jetPt=20.,
    jetEta=4.7,
    relaxJetId=False,  # relax = do not apply jet ID
    relaxPuJetId=True,  # relax = do not apply pileup jet ID
    jerCorr=False,
    # jesCorr = 1., # Shift jet energy scale in terms of uncertainties (1 = +1 sigma)
    puJetIDDisc='pileupJetId:fullDiscriminant',
)

metAna = cfg.Analyzer(
    METAnalyzer
)

vbfAna = cfg.Analyzer(
    VBFAnalyzer,
    name='VBFAnalyzer',
    cjvPtCut=20.,  # jet pT cut for central jet veto
    Mjj=500.,  # minimum dijet mass, only used for counting
    deltaEta=3.5  # minimum delta eta, only used for counting
)

recoilCorr = cfg.Analyzer(
    RecoilCorrector,
    name='RecoilCorrector',
    apply=False
)

embedWeighter = cfg.Analyzer(
    EmbedWeighter,
    name='EmbedWeighter',
    isRecHit=False,
    verbose=False
)

NJetsAna = cfg.Analyzer(
    NJetsAnalyzer,
    name='NJetsAnalyzer',
    fillTree=True,
    verbose=False
)

metFilter = cfg.Analyzer(
    METFilter,
    name='METFilter',
    processName='PAT',
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Moriond_2018
    triggers=[
        'Flag_goodVertices',
        'Flag_globalTightHalo2016Filter',
        'Flag_HBHENoiseFilter', 
        'Flag_HBHENoiseIsoFilter', 
        'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_BadPFMuonFilter',
        'Flag_BadChargedCandidateFilter',
        'Flag_eeBadScFilter',
        'Flag_ecalBadCalibFilter',
    ]
)

# higgsWeighter = cfg.Analyzer(
#     HiggsPtWeighter,
#     name='HiggsPtWeighter',
# )


###################################################
###                  SEQUENCE                   ###
###################################################
commonSequence = cfg.Sequence([
    lheWeightAna,
    jsonAna,
    skimAna,
    # genAna,
    # susyScanAna,
    triggerAna,  # First analyser that applies selections
    vertexAna,
    jetAna,
    metAna,
    httGenAna, # only relies on gen quantities
    httGenMatcher, # interpretation of event
    vbfAna,
    recoilCorr,
    pileUpAna,
    embedWeighter,
    NJetsAna,
    metFilter
    # higgsWeighter,
    # badCloneMuonAnaMoriond2017,
    # badMuonAnaMoriond2017
])
