import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

from CMGTools.H2TauTau.proto.analyzers.TauIsoAnalyzer import TauIsoAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauIsoTreeProducer import TauIsoTreeProducer
from CMGTools.H2TauTau.proto.samples.fall17.htt_common import DYJetsToLL_M50_LO, QCD_Pt_15to7000_TuneCP5_Flat2017, QCD_Pt_15to7000_TuneCP5_Flat
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA

production = getHeppyOption('production', True)

selected_components = [DYJetsToLL_M50_LO]
# selected_components = [QCD_Pt_15to7000_TuneCP5_Flat2017] ### THIS ONE IS BUGGY
# selected_components = [QCD_Pt_15to7000_TuneCP5_Flat]
autoAAA(selected_components)

tau_iso_ana = cfg.Analyzer(
    TauIsoAnalyzer,
    name='TauIsoAnalyzer',
    )

tau_iso_tree = cfg.Analyzer(
    TauIsoTreeProducer,
    name='TauIsoTreeProducer',
    defaultFloatType='F', #save storage space
    fill_all_pf=True,
    reject_gen_leptons=True
)

sequence = cfg.Sequence([
    tau_iso_ana,
    tau_iso_tree
])


if not production:
    selected_components = selected_components[:1]
    for comp in selected_components:
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
    # comp.files = comp.files[:1]
else:
    for comp in selected_components:
        comp.splitFactor = 500

config = cfg.Config(components=selected_components,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                   )

printComps(config.components, True)
