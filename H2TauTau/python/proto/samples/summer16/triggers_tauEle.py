# 2015 data and miniAOD v2
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerFilterMatch as TFM

data_triggers = [
    'HLT_Ele23_WPLoose_Gsf_v3',
    'HLT_Ele23_WPLoose_Gsf_v2',
    'HLT_Ele23_WPLoose_Gsf_v1',
    ]

data_triggerfilters = [
    'hltSingleEle23WPLooseGsfTrackIsoFilter'
]

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MSSMAHTauTauFull2016#Triggers
mc_triggers = [
    'HLT_Ele25_eta2p1_WPTight_Gsf_v1',
    ]

mc_triggerfilters = [
    TFM(leg1_names=['hltEle25erWPTightGsfTrackIsoFilter'], leg2_names=[], triggers=['HLT_Ele25_eta2p1_WPTight_Gsf_v1']),
]

embed_triggers = [
    ]
