import PhysicsTools.HeppyCore.framework.config as cfg
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

# ComponentCreator.useAAA = True
kreator = ComponentCreator()
comp = kreator.makeMCComponent(
    'HiggsSUSYBB1000',
    '/SUSYGluGluToBBHToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
    'CMS',
    '.*root',
    useAAA=False,
)

selectedComponents = [comp]

from PhysicsTools.Heppy.analyzers.core.EventSelector import EventSelector

eventSelector = cfg.Analyzer(
    EventSelector,
    toSelect = [
        1, 
        10,
        159
        ]
    )

sequence = cfg.Sequence([
        eventSelector
        ])

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    # preprocessor=preprocessor,
                    events_class=Events
                    )

print config
