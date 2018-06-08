import os

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

from ROOT import gSystem, gROOT
if "/sHTTEfficiencies_cc.so" not in gSystem.GetLibraries(): 
    gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/HTTEfficiencies.cc+" % os.environ['CMSSW_BASE']);
    from ROOT import getTauWeight, getTauIDWeightLoose, getTauIDWeightTight, getMuToTauWeightLoose, getMuToTauWeightTight, getEToTauWeightLoose, getEToTauWeightVLoose

class TauIDWeighter(Analyzer):

    def process(self, event):
        legs_to_process = self.cfg_ana.legs
        for legname in legs_to_process:
            leg = getattr(event, legname)
            if hasattr(self.cfg_ana,'channel') and self.cfg_ana.channel == 'mt':
                if leg.gen_match in [5]:
                    weight = getTauIDWeightTight(leg.pt(),leg.eta(),leg.decayMode()) # or loose WP ?
                elif leg.gen_match in [2,4]:
                    weight = getMuToTauWeightTight(leg.eta())
                elif leg.gen_match in [1,3]:
                    weight = getEToTauWeightVLoose(leg.eta()) # sur VLoose ? not Loose ?
                else:
                    weight = 1.
            else:
                weight = getTauWeight(leg.gen_match,
                                  leg.pt(),
                                  leg.eta(),
                                  leg.decayMode())

            setattr(event,'IDweight'+legname,weight)
            event.eventWeight*=weight
            
