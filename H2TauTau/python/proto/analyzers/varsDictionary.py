# change the branch names here

vars = {}

# Event ID
vars['run'] = {'std': 'run', 'sync': 'run'}
vars['lumi'] = {'std': 'lumi', 'sync': 'lumi'}
vars['event'] = {'std': 'evt', 'sync': 'evt'}

# Generator info
vars['geninfo_tt'] = {'std': 'geninfo_tt', 'sync': 'isZtt'}
vars['geninfo_mt'] = {'std': 'geninfo_mt', 'sync': 'isZmt'}
vars['geninfo_et'] = {'std': 'geninfo_et', 'sync': 'isZet'}
vars['geninfo_ee'] = {'std': 'geninfo_ee', 'sync': 'isZee'}
vars['geninfo_mm'] = {'std': 'geninfo_mm', 'sync': 'isZmm'}
vars['geninfo_em'] = {'std': 'geninfo_em', 'sync': 'isZem'}
vars['geninfo_EE'] = {'std': 'geninfo_EE', 'sync': 'isZEE'}
vars['geninfo_MM'] = {'std': 'geninfo_MM', 'sync': 'isZMM'}
vars['geninfo_LL'] = {'std': 'geninfo_LL', 'sync': 'isZLL'}
vars['geninfo_fakeid'] = {'std': 'geninfo_fakeid', 'sync': 'isFake'}

# Weights
vars['weight'] = {'std': 'weight', 'sync': 'weight'}
vars['weight_vertex'] = {'std': 'weight_pu', 'sync': 'puweight'}

# PileUp
vars['geninfo_nup'] = {'std': 'n_up', 'sync': 'NUP'}
vars['geninfo_invmass'] = {'std': 'gen_boson_mass', 'sync': 'geninvmass'}
vars['geninfo_htgen'] = {'std': 'gen_boson_pt', 'sync': 'gen_boson_pt'}
vars['n_vertices'] = {'std': 'n_pv', 'sync': 'npv'}
vars['npu'] = {'std': 'n_pu', 'sync': 'npu'}
vars['nPU'] = {'std': 'n_pu', 'sync': 'npu'}
vars['rho'] = {'std': 'rho', 'sync': 'rho'}

# Lepton vetoes
vars['veto_dilepton'] = {'std':'veto_dilepton', 'sync':'dilepton_veto'}
vars['veto_thirdlepton'] = {'std':'veto_thirdlepton', 'sync':'extramuon_veto'}
vars['veto_otherlepton'] = {'std':'veto_otherlepton', 'sync':'extraelec_veto'}


# Leg 1 (tau, mu, ele)
vars['l1_pt'] = {'std': 'l1_pt', 'sync': 'pt_1'}
vars['l1_eta'] = {'std': 'l1_eta', 'sync': 'eta_1'}
vars['l1_phi'] = {'std': 'l1_phi', 'sync': 'phi_1'}
vars['l1_mass'] = {'std': 'l1_m', 'sync': 'm_1'}
vars['l1_charge'] = {'std': 'l1_q', 'sync': 'q_1'}
vars['l1_reliso05'] = {'std': 'l1_iso', 'sync': 'iso_1'}
vars['l1_dxy'] = {'std': 'l1_d0', 'sync': 'd0_1'}
vars['l1_dz'] = {'std': 'l1_dz', 'sync': 'dZ_1'}
vars['mt'] = {'std': 'l1_mt', 'sync': 'mt_1'}
vars['puppimet_mt1'] = {'std': 'puppimet_mt1', 'sync': 'puppimt_1'}
vars['pfmet_mt1'] = {'std': 'pfmet_mt1', 'sync': 'pfmt_1'}
vars['l1_muonid_loose'] = {'std': 'l1_muonid_loose', 'sync': 'id_m_loose_1'}
vars['l1_muonid_medium'] = {'std': 'l1_muonid_medium', 'sync': 'id_m_medium_1'}
vars['l1_muonid_tight'] = {'std': 'l1_muonid_tight', 'sync': 'id_m_tight_1'}
vars['l1_muonid_tightnovtx'] = {'std': 'l1_muonid_tightnovtx', 'sync': 'id_m_tightnovtx_1'}
vars['l1_muonid_highpt'] = {'std': 'l1_muonid_highpt', 'sync': 'id_m_highpt_1'}
vars['l1_eid_nontrigmva_loose'] = {'std': 'l1_id_e_mva_nt_loose', 'sync': 'id_e_mva_nt_loose_1'}
vars['l1_eid_nontrigmva_tight'] = {'std': 'l1_eid_nontrigmva_tight', 'sync': 'id_e_mva_nt_tight_1'}
vars['l1_eid_veto'] = {'std': 'l1_eid_veto', 'sync': 'id_e_cut_veto_1'}
vars['l1_eid_loose'] = {'std': 'l1_eid_loose', 'sync': 'id_e_cut_loose_1'}
vars['l1_eid_medium'] = {'std': 'l1_eid_medium', 'sync': 'id_e_cut_medium_1'}
vars['l1_eid_tight'] = {'std': 'l1_eid_tight', 'sync': 'id_e_cut_tight_1'}
vars['l1_weight_trigger'] = {'std': 'l1_weight_trig', 'sync': 'trigweight_1'}
vars['l1_weight_tracking'] = {'std': 'l1_weight_tracking', 'sync': 'trackingweight_1'}
vars['l1_weight_idiso'] = {'std': 'l1_weight_idiso', 'sync': 'idisoweight_1'}
#vars['l1_weight'] = {'std': 'l1_weight', 'sync': 'effweight'}
vars['l1_againstElectronLooseMVA5'] = {'std': 'l1_againstElectronLooseMVA5', 'sync': 'againstElectronLooseMVA5_1'}
vars['l1_againstElectronMediumMVA5'] = {'std': 'l1_againstElectronMediumMVA5', 'sync': 'againstElectronMediumMVA5_1'}
vars['l1_againstElectronTightMVA5'] = {'std': 'l1_againstElectronTightMVA5', 'sync': 'againstElectronTightMVA5_1'}
vars['l1_againstElectronVLooseMVA5'] = {'std': 'l1_againstElectronVLooseMVA5', 'sync': 'againstElectronVLooseMVA5_1'}
vars['l1_againstElectronVTightMVA5'] = {'std': 'l1_againstElectronVTightMVA5', 'sync': 'againstElectronVTightMVA5_1'}
vars['l1_againstMuonLoose3'] = {'std': 'l1_againstMuonLoose3', 'sync': 'againstMuonLoose3_1'}
vars['l1_againstMuonTight3'] = {'std': 'l1_againstMuonTight3', 'sync': 'againstMuonTight3_1'}
vars['l1_byCombinedIsolationDeltaBetaCorrRaw3Hits'] = {'std': 'l1_byCombinedIsolationDeltaBetaCorrRaw3Hits', 'sync': 'byCombinedIsolationDeltaBetaCorrRaw3Hits_1'}
vars['l1_byIsolationMVArun2v1newDMwoLTraw'] = {'std': 'l1_byIsolationMVArun2v1newDMwoLTraw', 'sync': 'byIsolationMVArun2v1newDMwoLTraw_1'}
vars['l1_byIsolationMVArun2v1oldDMwoLTraw'] = {'std': 'l1_byIsolationMVArun2v1oldDMwoLTraw', 'sync': 'byIsolationMVArun2v1oldDMwoLTraw_1'}
vars['l1_byIsolationMVArun2v1newDMwLTraw'] = {'std': 'l1_byIsolationMVArun2v1newDMwLTraw', 'sync': 'byIsolationMVArun2v1newDMwLTraw_1'}
vars['l1_byIsolationMVArun2v1oldDMwLTraw'] = {'std': 'l1_byIsolationMVArun2v1oldDMwLTraw', 'sync': 'byIsolationMVArun2v1oldDMwLTraw_1'}
vars['l1_chargedIsoPtSum'] = {'std': 'l1_chargedIsoPtSum', 'sync': 'chargedIsoPtSum_1'}
vars['l1_decayModeFinding'] = {'std': 'l1_decayModeFindingOldDMs', 'sync': 'decayModeFindingOldDMs_1'}
vars['l1_decayModeFindingNewDMs'] = {'std': 'l1_decayModeFindingNewDMs', 'sync': 'decayModeFindingNewDMs_1'}
vars['l1_neutralIsoPtSum'] = {'std': 'l1_neutralIsoPtSum', 'sync': 'neutralIsoPtSum_1'}
vars['l1_puCorrPtSum'] = {'std': 'l1_puCorrPtSum', 'sync': 'puCorrPtSum_1'}
vars['l1_gen_match'] = {'std': 'l1_gen_match', 'sync': 'gen_match_1'}
vars['l1_byTightIsolationMVArun2v1DBoldDMwLT'] = {'std': 'l1_byTightIsolationMVArun2v1DBoldDMwLT', 'sync': 'byTightIsolationMVArun2v1DBoldDMwLT_1'}# For sync check
vars['l1_byVVLooseIsolationMVArun2017v2DBoldDMwLT2017'] = {'std': 'l1_byVVLooseIsolationMVArun2017v2DBoldDMwLT2017', 'sync': 'byVVLooseIsolationMVArun2017v2DBoldDMwLT2017_1'}
vars['l1_byVLooseIsolationMVArun2017v2DBoldDMwLT2017'] = {'std': 'l1_byVLooseIsolationMVArun2017v2DBoldDMwLT2017', 'sync': 'byVLooseIsolationMVArun2017v2DBoldDMwLT2017_1'}
vars['l1_byLooseIsolationMVArun2017v2DBoldDMwLT2017'] = {'std': 'l1_byLooseIsolationMVArun2017v2DBoldDMwLT2017', 'sync': 'byLooseIsolationMVArun2017v2DBoldDMwLT2017_1'}
vars['l1_byMediumIsolationMVArun2017v2DBoldDMwLT2017'] = {'std': 'l1_byMediumIsolationMVArun2017v2DBoldDMwLT2017', 'sync': 'byMediumIsolationMVArun2017v2DBoldDMwLT2017_1'}
vars['l1_byTightIsolationMVArun2017v2DBoldDMwLT2017'] = {'std': 'l1_byTightIsolationMVArun2017v2DBoldDMwLT2017', 'sync': 'byTightIsolationMVArun2017v2DBoldDMwLT2017_1'}
vars['l1_byVTightIsolationMVArun2017v2DBoldDMwLT2017'] = {'std': 'l1_byVTightIsolationMVArun2017v2DBoldDMwLT2017', 'sync': 'byVTightIsolationMVArun2017v2DBoldDMwLT2017_1'}
vars['l1_byVVTightIsolationMVArun2017v2DBoldDMwLT2017'] = {'std': 'l1_byVVTightIsolationMVArun2017v2DBoldDMwLT2017', 'sync': 'byVVTightIsolationMVArun2017v2DBoldDMwLT2017_1'}
vars['l1_byIsolationMVArun2017v2DBoldDMwLTraw2017'] = {'std': 'l1_byIsolationMVArun2017v2DBoldDMwLTraw2017', 'sync': 'byIsolationMVArun2017v2DBoldDMwLTraw2017_1'}

# Leg 2 (tau, mu, ele)
vars['l2_pt'] = {'std': 'l2_pt', 'sync': 'pt_2'}
vars['l2_phi'] = {'std': 'l2_phi', 'sync': 'phi_2'}
vars['l2_eta'] = {'std': 'l2_eta', 'sync': 'eta_2'}
vars['l2_mass'] = {'std': 'l2_m', 'sync': 'm_2'}
vars['l2_charge'] = {'std': 'l2_q', 'sync': 'q_2'}
vars['l2_dxy'] = {'std': 'l2_d0', 'sync': 'd0_2'}
vars['l2_dz'] = {'std': 'l2_dz', 'sync': 'dZ_2'}
vars['mt_leg2'] = {'std': 'l2_mt', 'sync': 'mt_2'}
vars['puppimet_mt2'] = {'std': 'puppimet_mt2', 'sync': 'puppimt_2'}
vars['pfmet_mt2'] = {'std': 'pfmet_mt2', 'sync': 'pfmt_2'}
vars['l2_reliso05'] = {'std': 'l2_iso', 'sync': 'iso_2'}
vars['l2_muonid_loose'] = {'std': 'l2_muonid_loose', 'sync': 'id_m_loose_2'}
vars['l2_muonid_medium'] = {'std': 'l2_muonid_medium', 'sync': 'id_m_medium_2'}
vars['l2_muonid_tight'] = {'std': 'l2_muonid_tight', 'sync': 'id_m_tight_2'}
vars['l2_muonid_tightnovtx'] = {'std': 'l2_muonid_tightnovtx', 'sync': 'id_m_tightnovtx_2'}
vars['l2_muonid_highpt'] = {'std': 'l2_muonid_highpt', 'sync': 'id_m_highpt_2'}
vars['l2_eid_nontrigmva_loose'] = {'std': 'l2_id_e_mva_nt_loose', 'sync': 'id_e_mva_nt_loose_2'}
vars['l2_eid_nontrigmva_tight'] = {'std': 'l2_eid_nontrigmva_tight', 'sync': 'id_e_mva_nt_loose_2'}
vars['l2_eid_veto'] = {'std': 'l2_eid_veto', 'sync': 'id_e_cut_veto_2'}
vars['l2_eid_loose'] = {'std': 'l2_eid_loose', 'sync': 'id_e_cut_loose_2'}
vars['l2_eid_medium'] = {'std': 'l2_eid_medium', 'sync': 'id_e_cut_medium_2'}
vars['l2_eid_tight'] = {'std': 'l2_eid_tight', 'sync': 'id_e_cut_tight_2'}
vars['l2_weight_trigger'] = {'std': 'l2_weight_trigger', 'sync': 'trigweight_2'}
vars['l2_weight_tracking'] = {'std': 'l2_weight_tracking', 'sync': 'trackingweight_2'}
vars['l2_againstElectronLooseMVA5'] = {'std': 'l2_againstElectronLooseMVA5', 'sync': 'againstElectronLooseMVA5_2'}
vars['l2_againstElectronMediumMVA5'] = {'std': 'l2_againstElectronMediumMVA5', 'sync': 'againstElectronMediumMVA5_2'}
vars['l2_againstElectronTightMVA5'] = {'std': 'l2_againstElectronTightMVA5', 'sync': 'againstElectronTightMVA5_2'}
vars['l2_againstElectronVLooseMVA5'] = {'std': 'l2_againstElectronVLooseMVA5', 'sync': 'againstElectronVLooseMVA5_2'}
vars['l2_againstElectronVTightMVA5'] = {'std': 'l2_againstElectronVTightMVA5', 'sync': 'againstElectronVTightMVA5_2'}
vars['l2_againstMuonLoose3'] = {'std': 'l2_againstMuonLoose3', 'sync': 'againstMuonLoose3_2'}
vars['l2_againstMuonTight3'] = {'std': 'l2_againstMuonTight3', 'sync': 'againstMuonTight3_2'}
vars['l2_byCombinedIsolationDeltaBetaCorrRaw3Hits'] = {'std': 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', 'sync': 'byCombinedIsolationDeltaBetaCorrRaw3Hits_2'}
vars['l2_byIsolationMVArun2v1newDMwoLTraw'] = {'std': 'l2_byIsolationMVArun2v1newDMwoLTraw', 'sync': 'byIsolationMVArun2v1newDMwoLTraw_2'}
vars['l2_byIsolationMVArun2v1oldDMwoLTraw'] = {'std': 'l2_byIsolationMVArun2v1oldDMwoLTraw', 'sync': 'byIsolationMVArun2v1oldDMwoLTraw_2'}
vars['l2_byIsolationMVArun2v1newDMwLTraw'] = {'std': 'l2_byIsolationMVArun2v1newDMwLTraw', 'sync': 'byIsolationMVArun2v1newDMwLTraw_2'}
vars['l2_byIsolationMVArun2v1oldDMwLTraw'] = {'std': 'l2_byIsolationMVArun2v1oldDMwLTraw', 'sync': 'byIsolationMVArun2v1oldDMwLTraw_2'}
vars['l2_chargedIsoPtSum'] = {'std': 'l2_chargedIsoPtSum', 'sync': 'chargedIsoPtSum_2'}
vars['l2_decayModeFinding'] = {'std': 'l2_decayModeFindingOldDMs', 'sync': 'decayModeFindingOldDMs_2'}
vars['l2_decayModeFindingNewDMs'] = {'std': 'l2_decayModeFindingNewDMs', 'sync': 'decayModeFindingNewDMs_2'}
vars['l2_neutralIsoPtSum'] = {'std': 'l2_neutralIsoPtSum', 'sync': 'neutralIsoPtSum_2'}
vars['l2_puCorrPtSum'] = {'std': 'l2_puCorrPtSum', 'sync': 'puCorrPtSum_2'}
vars['l2_gen_match'] = {'std': 'l2_gen_match', 'sync': 'gen_match_2'}
vars['l2_byTightIsolationMVArun2v1DBoldDMwLT'] = {'std': 'l2_byTightIsolationMVArun2v1DBoldDMwLT', 'sync': 'mva_olddm_tight_2'}# For sync check

# di-tau pair
vars['pthiggs'] = {'std': 'pthiggs', 'sync': 'pt_tt'}
vars['visMass'] = {'std': 'visMass', 'sync': 'm_vis'}
vars['mt_total'] = {'std': 'mt_tot', 'sync': 'mt_tot'}
vars['dil_pt'] = {'std': 'pt_tt', 'sync': 'pt_tt'}
vars['mvis'] = {'std': 'm_vis', 'sync': 'm_vis'}
vars['svfit_mass'] = {'std': 'm_sv', 'sync': 'm_sv'}
vars['svfit_transverse_mass'] = {'std':'mt_sv', 'sync':'mt_sv'}
vars['svfit_pt'] = {'std': 'svfit_pt', 'sync': 'pt_sv'}
vars['svfit_eta'] = {'std': 'svfit_eta', 'sync': 'eta_sv'}
vars['svfit_phi'] = {'std': 'svfit_phi', 'sync': 'phi_sv'}
vars['svfit_met'] = {'std': 'svfit_met', 'sync': 'met_sv'}

# MET
vars['pfmet_pt'] = {'std': 'pfmet', 'sync': 'met'}
vars['pfmet_phi'] = {'std': 'pfmet_phi', 'sync': 'metphi'}
vars['met_pt'] = {'std': 'met', 'sync': 'mvamet'}
vars['met_phi'] = {'std': 'met_phi', 'sync': 'mvametphi'}
vars['puppimet_pt'] = {'std': 'puppimet_pt', 'sync': 'puppimet'}
vars['puppimet_phi'] = {'std': 'puppimet_phi', 'sync': 'puppimetphi'}
vars['pzeta_vis'] = {'std': 'pzeta_vis', 'sync': 'pzetavis'}
vars['pzeta_met'] = {'std': 'pzeta_miss', 'sync': 'pzetamiss'}

vars['met_cov00'] = {'std': 'met_cov00', 'sync': 'mvacov00'}
vars['met_cov01'] = {'std': 'met_cov01', 'sync': 'mvacov01'}
vars['met_cov10'] = {'std': 'met_cov10', 'sync': 'mvacov10'}
vars['met_cov11'] = {'std': 'met_cov11', 'sync': 'mvacov11'}

# VBF
vars['vbf_mjj'] = {'std': 'mjj', 'sync': 'mjj'}
vars['vbf_dijetpt'] = {'std': 'dijetpt', 'sync': 'dijetpt'}
vars['vbf_dijetphi'] = {'std': 'dijetphi', 'sync': 'dijetphi'}
vars['vbf_ptvis'] = {'std': 'ptvis', 'sync': 'ptvis'}
vars['vbf_deta'] = {'std': 'jdeta', 'sync': 'jdeta'}
vars['vbf_jdphi'] = {'std': 'jdphi', 'sync': 'jdphi'}
vars['vbf_n_central'] = {'std': 'njetingap', 'sync': 'njetingap'}
# TODO check if name in code (H2tautautreeproducer) is vbf or ditau
# vars['ditau_mjj'] = {'std': 'ditau_mjj', 'sync': 'mjj'}
# vars['ditau_deta'] = {'std': 'ditau_deta', 'sync': 'jdeta'}
# vars['ditau_nCentral'] = {'std': 'ditau_n_central', 'sync': 'njetingap'}
# vars['ditau_nCentral'] = {'std': 'ditau_n_central20', 'sync': 'njetingap20'}
# vars['ditau_mva'] = {'std': 'ditau_mva', 'sync': 'mva'}

# vars['ditau_jdphi'] = {'std': 'ditau_jdphi', 'sync': 'jdphi'}
# vars['ditau_dijetpt'] = {'std': 'ditau_dijetpt', 'sync': 'dijetpt'}
# vars['ditau_dijetphi'] = {'std': 'ditau_dijetphi', 'sync': 'dijetphi'}
# vars['ditau_hdijetphi'] = {'std': 'ditau_hdijetphi', 'sync': 'hdijetphi'}
# vars['ditau_visjeteta'] = {'std': 'ditau_visjeteta', 'sync': 'visjeteta'}
# vars['ditau_ptvis'] = {'std': 'ditau_ptvis', 'sync': 'ptvis'}

# N Jets
vars['n_jets'] = {'std': 'n_jets', 'sync': 'njets'}
vars['n_jets_20'] = {'std': 'n_jets_20', 'sync': 'njetspt20'}
vars['n_bjets'] = {'std': 'n_bjets', 'sync': 'nbtag'}

# Jet 1
vars['jet1_pt'] = {'std': 'j1_pt', 'sync': 'jpt_1'}
vars['jet1_eta'] = {'std': 'j1_eta', 'sync': 'jeta_1'}
vars['jet1_phi'] = {'std': 'j1_phi', 'sync': 'jphi_1'}
vars['jet1_charge'] = {'std': 'j1_q', 'sync': 'jq_1'}
vars['jet1_mass'] = {'std': 'j1_m', 'sync': 'jm_1'}
vars['jet1_rawFactor'] = {'std': 'j1_rawf', 'sync': 'jrawf_1'}
vars['jet1_mva_pu'] = {'std': 'j1_mva_pu', 'sync': 'jmva_1'}
vars['jet1_flavour_parton'] = {'std': 'j1_flavour_parton', 'sync': 'j1_flavour_parton'}
vars['jet1_flavour_hadron'] = {'std': 'j1_flavour_hadron', 'sync': 'j1_flavour_hadron'}
vars['jet1_id_loose'] = {'std': 'jet1_id_loose', 'sync': 'jpfid_1'}
vars['jet1_id_pu'] = {'std': 'j1_puid', 'sync': 'jpuid_1'}
vars['jet1_csv'] = {'std': 'j1_bcsv', 'sync': 'jcsv_1'}

# Jet 2
vars['jet2_pt'] = {'std': 'j2_pt', 'sync': 'jpt_2'}
vars['jet2_eta'] = {'std': 'j2_eta', 'sync': 'jeta_2'}
vars['jet2_phi'] = {'std': 'j2_phi', 'sync': 'jphi_2'}
vars['jet2_charge'] = {'std': 'j2_q', 'sync': 'jq_2'}
vars['jet2_mass'] = {'std': 'j2_m', 'sync': 'jm_2'}
vars['jet2_rawFactor'] = {'std': 'j2_rawf', 'sync': 'jrawf_2'}
vars['jet2_mva_pu'] = {'std': 'j2_mva_pu', 'sync': 'jmva_2'}
vars['jet2_flavour_parton'] = {'std': 'j2_flavour_parton', 'sync': 'j2_flavour_parton'}
vars['jet2_flavour_hadron'] = {'std': 'j2_flavour_hadron', 'sync': 'j2_flavour_hadron'}
vars['jet2_id_loose'] = {'std': 'j2_id_loose', 'sync': 'jpfid_2'}
vars['jet2_id_pu'] = {'std': 'j2_puid', 'sync': 'jpuid_2'}
vars['jet2_csv'] = {'std': 'j2_bcsv', 'sync': 'jcsv_2'}

# bJet 1
vars['bjet1_pt'] = {'std': 'b1_pt', 'sync': 'bpt_1'}
vars['bjet1_eta'] = {'std': 'b1_eta', 'sync': 'beta_1'}
vars['bjet1_phi'] = {'std': 'b1_phi', 'sync': 'bphi_1'}
vars['bjet1_charge'] = {'std': 'b1_q', 'sync': 'bq_1'}
vars['bjet1_mass'] = {'std': 'b1_m', 'sync': 'bm_1'}
vars['bjet1_rawFactor'] = {'std': 'b1_rawf', 'sync': 'brawf_1'}
vars['bjet1_mva_pu'] = {'std': 'b1_mva_pu', 'sync': 'bmva_1'}
vars['bjet1_flavour_parton'] = {'std': 'b1_flavour_parton', 'sync': 'b1_flavour_parton'}
vars['bjet1_flavour_hadron'] = {'std': 'b1_flavour_hadron', 'sync': 'b1_flavour_hadron'}
vars['bjet1_id_loose'] = {'std': 'b1_id_loose', 'sync': 'bpfid_1'}
vars['bjet1_id_pu'] = {'std': 'b1_puid', 'sync': 'bpuid_1'}
vars['bjet1_csv'] = {'std': 'b1_bcsv', 'sync': 'bcsv_1'}

# bJet 2
vars['bjet2_pt'] = {'std': 'b2_pt', 'sync': 'bpt_2'}
vars['bjet2_eta'] = {'std': 'b2_eta', 'sync': 'beta_2'}
vars['bjet2_phi'] = {'std': 'b2_phi', 'sync': 'bphi_2'}
vars['bjet2_charge'] = {'std': 'b2_q', 'sync': 'bq_2'}
vars['bjet2_mass'] = {'std': 'b2_m', 'sync': 'bm_2'}
vars['bjet2_rawFactor'] = {'std': 'b2_rawf', 'sync': 'brawf_2'}
vars['bjet2_mva_pu'] = {'std': 'b2_mva_pu', 'sync': 'bmva_2'}
vars['bjet2_flavour_parton'] = {'std': 'b2_flavour_parton', 'sync': 'b2_flavour_parton'}
vars['bjet2_flavour_hadron'] = {'std': 'b2_flavour_hadron', 'sync': 'b2_flavour_hadron'}
vars['bjet2_id_loose'] = {'std': 'b2_id_loose', 'sync': 'bpfid_2'}
vars['bjet2_id_pu'] = {'std': 'b2_puid', 'sync': 'bpuid_2'}
vars['bjet2_csv'] = {'std': 'b2_bcsv', 'sync': 'bcsv_2'}

# trigger names
#vars['trigger_matched_isomu22'] = {'std':'trigger_matched_isomu22', 'sync':'trg_singlemuon'} #?
vars['trigger_matched_singlemuon'] = {'std':'trigger_matched_singlemuon', 'sync':'trg_singlemuon'}

vars['trigger_ditau35'] = {'std':'trigger_ditau35', 'sync':'trg_fired_doubletau'}
vars['trigger_ditau35_combiso'] = {'std':'trigger_ditau35_combiso', 'sync':'trg_fired_doubletau_combiso'}
vars['trigger_singletau140'] = {'std':'trigger_singletau140', 'sync':'trg_fired_singletau'}
vars['trigger_singletau120'] = {'std':'trigger_singletau120', 'sync':'trg_fired_singletau120'}

vars['trigger_matched_ditau35'] = {'std':'trigger_matched_ditau35', 'sync':'trg_doubletau'}
vars['trigger_matched_ditau35_combiso'] = {'std':'trigger_matched_ditau35_combiso', 'sync':'trg_doubletau_combiso'}
vars['trigger_matched_singletau140'] = {'std':'trigger_matched_singletau140', 'sync':'trg_singletau'}
vars['trigger_matched_singletau120'] = {'std':'trigger_matched_singletau120', 'sync':'trg_singletau120'}
