from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

kreator = ComponentCreator()

json = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'

# ----------------------------- Run2017B 31Mar2018 ----------------------------------------

JetHT_Run2017B_31Mar2018 = kreator.makeDataComponent("JetHT_Run2017B_31Mar2018", "/JetHT/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017B_31Mar2018 = kreator.makeDataComponent("HTMHT_Run2017B_31Mar2018", "/HTMHT/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017B_31Mar2018 = kreator.makeDataComponent("MET_Run2017B_31Mar2018", "/MET/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017B_31Mar2018 = kreator.makeDataComponent("SingleElectron_Run2017B_31Mar2018", "/SingleElectron/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017B_31Mar2018 = kreator.makeDataComponent("SingleMuon_Run2017B_31Mar2018", "/SingleMuon/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017B_31Mar2018 = kreator.makeDataComponent("SinglePhoton_Run2017B_31Mar2018", "/SinglePhoton/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017B_31Mar2018 = kreator.makeDataComponent("DoubleEG_Run2017B_31Mar2018", "/DoubleEG/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017B_31Mar2018 = kreator.makeDataComponent("MuonEG_Run2017B_31Mar2018", "/MuonEG/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017B_31Mar2018 = kreator.makeDataComponent("DoubleMuon_Run2017B_31Mar2018", "/DoubleMuon/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017B_31Mar2018 = kreator.makeDataComponent("Tau_Run2017B_31Mar2018", "/Tau/Run2017B-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017B_31Mar2018 = [JetHT_Run2017B_31Mar2018, HTMHT_Run2017B_31Mar2018, MET_Run2017B_31Mar2018, SingleElectron_Run2017B_31Mar2018, SingleMuon_Run2017B_31Mar2018, SinglePhoton_Run2017B_31Mar2018, DoubleEG_Run2017B_31Mar2018, MuonEG_Run2017B_31Mar2018, DoubleMuon_Run2017B_31Mar2018, Tau_Run2017B_31Mar2018]

# ----------------------------- Run2017C 31Mar2018 ----------------------------------------

JetHT_Run2017C_31Mar2018 = kreator.makeDataComponent("JetHT_Run2017C_31Mar2018", "/JetHT/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017C_31Mar2018 = kreator.makeDataComponent("HTMHT_Run2017C_31Mar2018", "/HTMHT/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017C_31Mar2018 = kreator.makeDataComponent("MET_Run2017C_31Mar2018", "/MET/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017C_31Mar2018 = kreator.makeDataComponent("SingleElectron_Run2017C_31Mar2018", "/SingleElectron/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017C_31Mar2018 = kreator.makeDataComponent("SingleMuon_Run2017C_31Mar2018", "/SingleMuon/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017C_31Mar2018 = kreator.makeDataComponent("SinglePhoton_Run2017C_31Mar2018", "/SinglePhoton/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017C_31Mar2018 = kreator.makeDataComponent("DoubleEG_Run2017C_31Mar2018", "/DoubleEG/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017C_31Mar2018 = kreator.makeDataComponent("MuonEG_Run2017C_31Mar2018", "/MuonEG/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017C_31Mar2018 = kreator.makeDataComponent("DoubleMuon_Run2017C_31Mar2018", "/DoubleMuon/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017C_31Mar2018 = kreator.makeDataComponent("Tau_Run2017C_31Mar2018", "/Tau/Run2017C-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017C_31Mar2018 = [JetHT_Run2017C_31Mar2018, HTMHT_Run2017C_31Mar2018, MET_Run2017C_31Mar2018, SingleElectron_Run2017C_31Mar2018, SingleMuon_Run2017C_31Mar2018, SinglePhoton_Run2017C_31Mar2018, DoubleEG_Run2017C_31Mar2018, MuonEG_Run2017C_31Mar2018, DoubleMuon_Run2017C_31Mar2018, Tau_Run2017C_31Mar2018]


# ----------------------------- Run2017D 31Mar2018 ----------------------------------------

JetHT_Run2017D_31Mar2018 = kreator.makeDataComponent("JetHT_Run2017D_31Mar2018", "/JetHT/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017D_31Mar2018 = kreator.makeDataComponent("HTMHT_Run2017D_31Mar2018", "/HTMHT/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017D_31Mar2018 = kreator.makeDataComponent("MET_Run2017D_31Mar2018", "/MET/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017D_31Mar2018 = kreator.makeDataComponent("SingleElectron_Run2017D_31Mar2018", "/SingleElectron/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017D_31Mar2018 = kreator.makeDataComponent("SingleMuon_Run2017D_31Mar2018", "/SingleMuon/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017D_31Mar2018 = kreator.makeDataComponent("SinglePhoton_Run2017D_31Mar2018", "/SinglePhoton/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017D_31Mar2018 = kreator.makeDataComponent("DoubleEG_Run2017D_31Mar2018", "/DoubleEG/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017D_31Mar2018 = kreator.makeDataComponent("MuonEG_Run2017D_31Mar2018", "/MuonEG/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017D_31Mar2018 = kreator.makeDataComponent("DoubleMuon_Run2017D_31Mar2018", "/DoubleMuon/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017D_31Mar2018 = kreator.makeDataComponent("Tau_Run2017D_31Mar2018", "/Tau/Run2017D-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017D_31Mar2018 = [JetHT_Run2017D_31Mar2018, HTMHT_Run2017D_31Mar2018, MET_Run2017D_31Mar2018, SingleElectron_Run2017D_31Mar2018, SingleMuon_Run2017D_31Mar2018, SinglePhoton_Run2017D_31Mar2018, DoubleEG_Run2017D_31Mar2018, MuonEG_Run2017D_31Mar2018, DoubleMuon_Run2017D_31Mar2018, Tau_Run2017D_31Mar2018]

# ----------------------------- Run2017E 31Mar2018 ----------------------------------------

JetHT_Run2017E_31Mar2018 = kreator.makeDataComponent("JetHT_Run2017E_31Mar2018", "/JetHT/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017E_31Mar2018 = kreator.makeDataComponent("HTMHT_Run2017E_31Mar2018", "/HTMHT/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017E_31Mar2018 = kreator.makeDataComponent("MET_Run2017E_31Mar2018", "/MET/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017E_31Mar2018 = kreator.makeDataComponent("SingleElectron_Run2017E_31Mar2018", "/SingleElectron/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017E_31Mar2018 = kreator.makeDataComponent("SingleMuon_Run2017E_31Mar2018", "/SingleMuon/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017E_31Mar2018 = kreator.makeDataComponent("SinglePhoton_Run2017E_31Mar2018", "/SinglePhoton/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017E_31Mar2018 = kreator.makeDataComponent("DoubleEG_Run2017E_31Mar2018", "/DoubleEG/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017E_31Mar2018 = kreator.makeDataComponent("MuonEG_Run2017E_31Mar2018", "/MuonEG/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017E_31Mar2018 = kreator.makeDataComponent("DoubleMuon_Run2017E_31Mar2018", "/DoubleMuon/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017E_31Mar2018 = kreator.makeDataComponent("Tau_Run2017E_31Mar2018", "/Tau/Run2017E-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017E_31Mar2018 = [JetHT_Run2017E_31Mar2018, HTMHT_Run2017E_31Mar2018, MET_Run2017E_31Mar2018, SingleElectron_Run2017E_31Mar2018, SingleMuon_Run2017E_31Mar2018, SinglePhoton_Run2017E_31Mar2018, DoubleEG_Run2017E_31Mar2018, MuonEG_Run2017E_31Mar2018, DoubleMuon_Run2017E_31Mar2018, Tau_Run2017E_31Mar2018]


# ----------------------------- Run2017F 31Mar2018 ----------------------------------------

JetHT_Run2017F_31Mar2018 = kreator.makeDataComponent("JetHT_Run2017F_31Mar2018", "/JetHT/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
HTMHT_Run2017F_31Mar2018 = kreator.makeDataComponent("HTMHT_Run2017F_31Mar2018", "/HTMHT/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MET_Run2017F_31Mar2018 = kreator.makeDataComponent("MET_Run2017F_31Mar2018", "/MET/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleElectron_Run2017F_31Mar2018 = kreator.makeDataComponent("SingleElectron_Run2017F_31Mar2018", "/SingleElectron/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2017F_31Mar2018 = kreator.makeDataComponent("SingleMuon_Run2017F_31Mar2018", "/SingleMuon/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
SinglePhoton_Run2017F_31Mar2018 = kreator.makeDataComponent("SinglePhoton_Run2017F_31Mar2018", "/SinglePhoton/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleEG_Run2017F_31Mar2018 = kreator.makeDataComponent("DoubleEG_Run2017F_31Mar2018", "/DoubleEG/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2017F_31Mar2018 = kreator.makeDataComponent("MuonEG_Run2017F_31Mar2018", "/MuonEG/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2017F_31Mar2018 = kreator.makeDataComponent("DoubleMuon_Run2017F_31Mar2018", "/DoubleMuon/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)
Tau_Run2017F_31Mar2018 = kreator.makeDataComponent("Tau_Run2017F_31Mar2018", "/Tau/Run2017F-31Mar2018-v1/MINIAOD", "CMS", ".*root", json)

dataSamples_Run2017F_31Mar2018 = [JetHT_Run2017F_31Mar2018, HTMHT_Run2017F_31Mar2018, MET_Run2017F_31Mar2018, SingleElectron_Run2017F_31Mar2018, SingleMuon_Run2017F_31Mar2018, SinglePhoton_Run2017F_31Mar2018, DoubleEG_Run2017F_31Mar2018, MuonEG_Run2017F_31Mar2018, DoubleMuon_Run2017F_31Mar2018, Tau_Run2017F_31Mar2018]


data_single_muon = [SingleMuon_Run2017B_31Mar2018, SingleMuon_Run2017C_31Mar2018, SingleMuon_Run2017D_31Mar2018, SingleMuon_Run2017E_31Mar2018, SingleMuon_Run2017F_31Mar2018]
data_single_electron = [SingleElectron_Run2017B_31Mar2018, SingleElectron_Run2017C_31Mar2018, SingleElectron_Run2017D_31Mar2018, SingleElectron_Run2017E_31Mar2018, SingleElectron_Run2017F_31Mar2018]
data_muon_electron = [MuonEG_Run2017B_31Mar2018, MuonEG_Run2017C_31Mar2018, MuonEG_Run2017D_31Mar2018, MuonEG_Run2017E_31Mar2018, MuonEG_Run2017F_31Mar2018]
data_tau = [Tau_Run2017B_31Mar2018, Tau_Run2017C_31Mar2018, Tau_Run2017D_31Mar2018, Tau_Run2017E_31Mar2018, Tau_Run2017F_31Mar2018]
