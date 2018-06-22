import os

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

from ROOT import gSystem, gROOT
# if "/sHTTEfficiencies_cc.so" not in gSystem.GetLibraries(): 
#     gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/HTTEfficiencies.cc+" % os.environ['CMSSW_BASE']);
# gSystem.Load("libCMGToolsH2TauTau")
from ROOT import getTauWeight

class TauIDWeighter(Analyzer):

    def process(self, event):
        legs_to_process = self.cfg_ana.legs
        channel = self.cfg_ana.channel
        ele_WP  = self.cfg_ana.ele_WP
        mu_WP   = self.cfg_ana.mu_WP
        tau_WP  = self.cfg_ana.tau_WP
        for legname in legs_to_process:
            leg = getattr(event, legname)
            weight = getTauWeight(leg.gen_match,
                                  leg.pt(),
                                  leg.eta(),
                                  leg.decayMode(),
                                  ele_WP,
                                  mu_WP,
                                  tau_WP)

            setattr(event,'IDweight'+legname,weight)
            event.eventWeight*=weight
            
