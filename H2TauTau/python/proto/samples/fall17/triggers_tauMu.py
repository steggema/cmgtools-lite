from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerFilterMatch as TFM

# 2016 data
data_triggers = [
    'HLT_IsoMu24_v*',
    'HLT_IsoMu27_v*',
    'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*',
    # 'HLT_IsoMu24_eta2p1_v*',
    # 'HLT_IsoMu20_v*'
    # 'HLT_IsoTkMu24_v5',
    # 'HLT_IsoTkMu24_v4',
    # 'HLT_IsoTkMu24_v3',
    # 'HLT_IsoTkMu24_v2',
    # 'HLT_IsoTkMu24_v1',
    # 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v1',
    # 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v2',
    # 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v3',
    # 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v5',
    # 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v1',
    # 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v2',
    # 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v3',
    # 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v5',
    # 'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v1', # runs 274748-276244
    # 'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v2', # runs 276271-278240
    # 'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v3', # runs 278270-280960
    # 'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v5', # runs 281010-284044
    ]

data_triggerfilters = [
    TFM(leg1_names=['hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07'], leg2_names=[], triggers=['HLT_IsoMu24_v*']), # IsoMu24
    TFM(leg1_names=['hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07'], leg2_names=[], triggers=['HLT_IsoMu27_v*']), # IsoMu27
    TFM(leg1_names=['hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'], leg2_names=['hltSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'], triggers=['HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*'], match_all_names_leg1=True, match_all_names_leg2=True), # HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1
    # TFM(leg1_names=['hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09'], leg2_names=[], triggers=['HLT_IsoTkMu24_v1', 'HLT_IsoTkMu24_v2', 'HLT_IsoTkMu24_v3', 'HLT_IsoTkMu24_v4', 'HLT_IsoTkMu24_v5']), # IsoTkMu24
    # TFM(leg1_names=['hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09'], leg2_names=['hltOverlapFilterIsoMu19LooseIsoPFTau20'], triggers=['HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v2', 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v2', 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v3', 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v5']), # IsoMu19_eta2p1_LooseIsoPFTau20
    # TFM(leg1_names=['hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09'], leg2_names=['hltOverlapFilterIsoMu19LooseIsoPFTau20'], triggers=['HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v1', 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v2', 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v3', 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v5']), # IsoMu19_eta2p1_LooseIsoPFTau20
    # TFM(leg1_names=['hltPFTau140TrackPt50LooseAbsOrRelVLooseIso'], leg2_names=['hltPFTau140TrackPt50LooseAbsOrRelVLooseIso'], match_both_legs=False)
]

mc_triggers = [
    'HLT_IsoMu24_v*',
    # 'HLT_IsoMu24_v10',
    # 'HLT_IsoMu24_eta2p1_v12',
    # 'HLT_IsoMu27_v*'
    # 'HLT_IsoTkMu24_v4',
    # 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v5',
    # 'HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v5',
    # 'HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v5',
    'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*',
    # 'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v5',
    # 'HLT_VLooseIsoPFTau120_Trk50_eta2p1_v5',
    ]

mc_triggerfilters = [
    TFM(leg1_names=['hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07'], leg2_names=[], triggers=['HLT_IsoMu24_v*']), # IsoMu24
    TFM(leg1_names=['hltSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'], leg2_names=['hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'], triggers=['HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*'], match_all_names_leg1=True, match_all_names_leg2=True), # IsoMu19_eta2p1_LooseIsoPFTau20
    # TFM(leg1_names=['hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07'], leg2_names=[], triggers=['HLT_IsoMu27_v*']), # IsoMu24
    
    # TFM(leg1_names=['hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09'], leg2_names=[], triggers=['HLT_IsoTkMu24_v4']), # IsoTkMu24
    # TFM(leg1_names=['hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09'], leg2_names=['hltOverlapFilterIsoMu19LooseIsoPFTau20'], triggers=['HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v5']), # IsoMu19_eta2p1_LooseIsoPFTau20
    # TFM(leg1_names=['hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09'], leg2_names=['hltOverlapFilterIsoMu19LooseIsoPFTau20'], triggers=['HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v5']), # IsoMu19_eta2p1_LooseIsoPFTau20
    # TFM(leg1_names=['hltL3crIsoL1sSingleMu20erIorSingleMu22erL1f0L2f10QL3f21QL3trkIsoFiltered0p09'], leg2_names=['hltOverlapFilterIsoMu19LooseIsoPFTau20'], triggers=['HLT_IsoMu21_eta2p1_LooseIsoPFTau20_SingleL1_v5']), # IsoMu21_eta2p1_LooseIsoPFTau20
    # TFM(leg1_names=['hltPFTau140TrackPt50LooseAbsOrRelVLooseIso'], leg2_names=['hltPFTau140TrackPt50LooseAbsOrRelVLooseIso'], match_both_legs=False, triggers=['HLT_VLooseIsoPFTau140_Trk50_eta2p1_v5']),
    # TFM(leg1_names=['hltPFTau120TrackPt50LooseAbsOrRelVLooseIso'], leg2_names=['hltPFTau120TrackPt50LooseAbsOrRelVLooseIso'], match_both_legs=False, triggers=['HLT_VLooseIsoPFTau120_Trk50_eta2p1_v5'])

]

embed_triggers = [
    ]
