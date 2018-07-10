from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import DYNJetsToLL, QCD_EMs, TBar_tch, Ws, T_tch, DYJetsToLL_M10to50_LO, DYJetsToLL_M50_LO, DYJetsToLL_M50_LO_ext, TBar_tWch_noFullyHad, T_tWch_noFullyHad, WJetsToLNu_LO, TTLep_pow, TTHad_pow, TTSemi_pow, ZZTo4L,  WWTo2L2Nu, WZTo3LNu_fxfx, ZZTo2L2Nu, QCD_Pt_15to7000_TuneCP5_Flat2017, QCD_Pt_15to7000_TuneCP5_Flat

# There in 2016, not yet in 2017: QCDPtbcToE, WZJToLLLNu, WZTo1L3Nu, WWTo1L1Nu2Q, WZTo1L1Nu2Q, ZZTo2L2Q, WZTo2L2Q

from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import SingleMuon_Run2017B_31Mar2018, SingleElectron_Run2017B_31Mar2018, MuonEG_Run2017B_31Mar2018, Tau_Run2017B_31Mar2018
from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import SingleMuon_Run2017C_31Mar2018, SingleElectron_Run2017C_31Mar2018, MuonEG_Run2017C_31Mar2018, Tau_Run2017C_31Mar2018
from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import SingleMuon_Run2017D_31Mar2018, SingleElectron_Run2017D_31Mar2018, MuonEG_Run2017D_31Mar2018, Tau_Run2017D_31Mar2018
from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import SingleMuon_Run2017E_31Mar2018, SingleElectron_Run2017E_31Mar2018, MuonEG_Run2017E_31Mar2018, Tau_Run2017E_31Mar2018
from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import SingleMuon_Run2017F_31Mar2018, SingleElectron_Run2017F_31Mar2018, MuonEG_Run2017F_31Mar2018, Tau_Run2017F_31Mar2018

from CMGTools.H2TauTau.proto.samples.fall17.higgs import HiggsGGH125, HiggsVBF125, HiggsTTH125
from CMGTools.H2TauTau.proto.samples.fall17.higgs_susy import mc_higgs_susy_gg, mc_higgs_susy_bb

from CMGTools.H2TauTau.proto.samples.fall17.higgs_susy import HiggsSUSYBB900 as bbh900

# Full 2016
json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
lumi = 41298.

# Set cross sections to HTT values

# WWTo1L1Nu2Q.xSection = 49.997
# ZZTo2L2Q.xSection = 3.22
# ZZTo4L.xSection = 1.212 # Take the one from samples file, 1.256
# WZTo3LNu_fxfx.xSection = 5.26 # Take the one from sample file, 5.063
# WZTo2L2Q.xSection = 5.595
# WZTo1L3Nu.xSection = 3.05
# WZTo1L1Nu2Q.xSection = 10.71

w_xsec = 61526.7
dy_xsec = 5765.4

DYJetsToLL_M50_LO.xSection = dy_xsec
DYJetsToLL_M50_LO_ext.xSection = dy_xsec
# DYJetsToLL_M50.xSection = dy_xsec


# From https://twiki.cern.ch/twiki/pub/CMS/HiggsToTauTauWorking2015/DYNjetWeights.xls r3
# dy_weight_dict = {
#     (0, 0): 0.669144882/dy_xsec,
#     (0, 150): 0.001329134/dy_xsec,
#     (1, 0): 0.018336763/dy_xsec,
#     (1, 150): 0.001241603/dy_xsec,
#     (2, 0): 0.019627356/dy_xsec,
#     (2, 150): 0.001247156/dy_xsec,
#     (3, 0): 0.021024291/dy_xsec,
#     (3, 150): 0.001252443/dy_xsec,
#     (4, 0): 0.015530181/dy_xsec,
#     (4, 150): 0.001226594/dy_xsec,
# }

n_ev_dy_incl = 48099551.0 + 48744812.0
n_ev_dy_1jet = 32528702.0 + 34135231.0
n_ev_dy_2jet = 11611398.0 + 9691457.0
n_ev_dy_3jet = 4772102.0
n_ev_dy_4jet = 4327065.0


k_factor = dy_xsec/4954.0
dy_xsec_incl = 4954.0 * k_factor
dy_xsec_1jet = 878 * k_factor
dy_xsec_2jet = 307 * k_factor
dy_xsec_3jet = 112 * k_factor
dy_xsec_4jet = 44.2 * k_factor


dy_weight_dict = {
    0:dy_xsec_incl/n_ev_dy_incl,
    1:dy_xsec_1jet/(n_ev_dy_incl*dy_xsec_1jet/dy_xsec_incl + n_ev_dy_1jet),
    2:dy_xsec_2jet/(n_ev_dy_incl*dy_xsec_2jet/dy_xsec_incl  + n_ev_dy_2jet),
    3:dy_xsec_3jet/(n_ev_dy_incl*dy_xsec_3jet/dy_xsec_incl  + n_ev_dy_3jet),
    4:dy_xsec_4jet/(n_ev_dy_incl*dy_xsec_4jet/dy_xsec_incl  + n_ev_dy_4jet),
}

def getDYWeight(n_jets): # , m_gen): # mass > 150 GeV sample buggy...
    # if m_gen > 150.:
    #     return dy_weight_dict[(n_jets, 150)]
    return dy_weight_dict[n_jets]

for sample in [DYJetsToLL_M50_LO, DYJetsToLL_M50_LO_ext] + DYNJetsToLL: # + [DYJetsToTauTau_M150_LO]:
    # sample.fractions = [0.7, 0.204374, 0.0671836, 0.0205415, 0.0110539]

    sample.weight_func = getDYWeight
    sample.xSection = dy_xsec

# From https://twiki.cern.ch/twiki/pub/CMS/HiggsToTauTauWorking2015/DYNjetWeights.xls r3
w_weight_dict = {
    0:1.304600668/w_xsec,
    1:0.216233816/w_xsec,
    2:0.115900663/w_xsec,
    3:0.058200264/w_xsec,
    4:0.06275589/w_xsec
}

def getWWeight(n_jets):
    return w_weight_dict[n_jets]

for sample in [WJetsToLNu_LO] + Ws: # 

    sample.weight_func = getWWeight
    # sample.xSection = w_xsec

WJetsHT = [] # WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf

# Backgrounds
diboson_nlo = [ZZTo4L, WWTo2L2Nu, WZTo3LNu_fxfx, ZZTo2L2Nu]

essential = [TTLep_pow, TTHad_pow, TTSemi_pow, DYJetsToLL_M50_LO, DYJetsToLL_M50_LO_ext, DYJetsToLL_M10to50_LO, TBar_tWch_noFullyHad, T_tWch_noFullyHad, TBar_tch, T_tch, WJetsToLNu_LO]  # WJetsToLNu, 

# Build default background list
backgrounds = essential
backgrounds += DYNJetsToLL
# backgrounds += [DYJetsToTauTau_M150_LO, DYJetsToLL_M10to50_ext1]
backgrounds += Ws
backgrounds += diboson_nlo
backgrounds += []

backgrounds_mu = backgrounds[:]
# backgrounds_mu += [QCD_Mu15]

backgrounds_ele = backgrounds[:]
backgrounds_ele += QCD_EMs
# backgrounds_ele += QCDPtbcToE

# Data
data_single_muon = [SingleMuon_Run2017B_31Mar2018, SingleMuon_Run2017C_31Mar2018, SingleMuon_Run2017D_31Mar2018, SingleMuon_Run2017E_31Mar2018, SingleMuon_Run2017F_31Mar2018]
data_single_electron = [SingleElectron_Run2017B_31Mar2018, SingleElectron_Run2017C_31Mar2018, SingleElectron_Run2017D_31Mar2018, SingleElectron_Run2017E_31Mar2018, SingleElectron_Run2017F_31Mar2018]
data_muon_electron = [MuonEG_Run2017B_31Mar2018, MuonEG_Run2017C_31Mar2018, MuonEG_Run2017D_31Mar2018, MuonEG_Run2017E_31Mar2018, MuonEG_Run2017F_31Mar2018]
data_tau = [Tau_Run2017B_31Mar2018, Tau_Run2017C_31Mar2018, Tau_Run2017D_31Mar2018, Tau_Run2017E_31Mar2018, Tau_Run2017F_31Mar2018]

for sample in data_single_muon + data_single_electron + data_muon_electron + data_tau:
    sample.json = json
    sample.lumi = lumi

# Signals
sm_signals = [HiggsGGH125, HiggsVBF125, HiggsTTH125]
mssm_signals = mc_higgs_susy_bb + mc_higgs_susy_gg

sync_list = [bbh900, HiggsVBF125]
sync_list = [DYJetsToLL_M50_LO]
