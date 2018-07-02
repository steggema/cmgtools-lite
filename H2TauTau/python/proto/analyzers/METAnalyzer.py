import math

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

import ROOT
LorentzVector = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzE4D("double"))

class METAnalyzer(Analyzer):
    def declareHandles(self):
        super(METAnalyzer, self).declareHandles()
        self.handles['puppiMET'] = AutoHandle(
            'slimmedMETsPuppi',
            'std::vector<pat::MET>'
        )

        self.handles['pfMET'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )


    def process(self, event):
        self.readCollections(event.input)

        event.pfmet = self.handles['pfMET'].product()[0]
        event.puppimet = self.handles['puppiMET'].product()[0]
        
        if hasattr(event, 'metShift'):
            px_new = event.metShift[0] + event.pfmet.px()
            py_new = event.metShift[1] + event.pfmet.py()
            event.pfmet.setP4(LorentzVector(px_new, py_new, 0., math.sqrt(px_new*px_new + py_new*py_new)))

        return True
