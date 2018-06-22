import copy

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()
dbsInstance='phys03'

HiggsSUSYBB1000 = creator.makeMCComponent(
    "HiggsSUSYBB1000", 
    "/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER", 
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)


mc_higgs_susy_gg = [
 
]

mc_higgs_susy_bb = [
    HiggsSUSYBB1000,
]

mc_higgs_susy = copy.copy(mc_higgs_susy_gg)
mc_higgs_susy.extend(mc_higgs_susy_bb)
