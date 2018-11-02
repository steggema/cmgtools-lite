from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerFilterMatch as TFM

# 2016 data
data_triggers = [
    'HLT_IsoMu24_v*',
    'HLT_IsoMu27_v*',
    'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*'
    ]

data_triggerfilters = [
    # IsoMu24
    TFM(leg1_names=['hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07'], 
        leg2_names=[], 
        triggers=['HLT_IsoMu24_v*']),

    # IsoMu27
    TFM(leg1_names=['hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07'], 
        leg2_names=[], 
        triggers=['HLT_IsoMu27_v*']), 

    
    TFM(leg1_names=['hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'],
        leg2_names=['hltSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'],
        triggers=['HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*'], 
        match_all_names_leg1=True, 
        match_all_names_leg2=True),
]

mc_triggers = [
    'HLT_IsoMu24_v*',
    'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*',
    ]

mc_triggerfilters = [
    # IsoMu24
    TFM(leg1_names=['hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07'], 
        leg2_names=[], 
        triggers=['HLT_IsoMu24_v*']), 
    
    # IsoMu19_eta2p1_LooseIsoPFTau20
    TFM(leg1_names=['hltSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'], 
        leg2_names=['hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'], 
        triggers=['HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*'], 
        match_all_names_leg1=True, 
        match_all_names_leg2=True), 

]

embed_triggers = [
    ]
