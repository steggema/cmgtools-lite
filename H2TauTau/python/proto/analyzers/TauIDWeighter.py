import os

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

from ROOT import gSystem, gROOT
if "/sHTTEfficiencies_cc.so" not in gSystem.GetLibraries(): 
    gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/HTTEfficiencies.cc+" % os.environ['CMSSW_BASE']);
    from ROOT import getTauWeight

class TauIDWeighter(Analyzer):

    def process(self, event):
        legs_to_process = self.cfg_ana.legs
        for legname in legs_to_process:
            leg = getattr(event, legname)
            weight = getTauWeight(leg.gen_match,
                                  leg.pt(),
                                  leg.eta(),
                                  leg.decayMode())
            setattr(event,'IDweight'+legname,weight)
            event.eventWeight*=weight
