from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.statistics.average import Average

from CMGTools.H2TauTau.proto.weights.ScaleFactor import ScaleFactor


class LeptonWeighter(Analyzer):

    '''Gets lepton efficiency weight and puts it in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LeptonWeighter, self).__init__(cfg_ana, cfg_comp, looperName)

        self.leptonName = self.cfg_ana.lepton
        
        self.scaleFactors = {}
        for sf_name, sf_file in self.cfg_ana.scaleFactorFiles.items():
            if isinstance(sf_file, tuple):
                self.scaleFactors[sf_name] = ScaleFactor(sf_file[0], sf_file[1])
            else:
                self.scaleFactors[sf_name] = ScaleFactor(sf_file)
        if hasattr(self.cfg_ana, 'otherScaleFactorFiles'):
            for sf_name, sf_file in self.cfg_ana.otherScaleFactorFiles.items():
                if isinstance(sf_file, tuple):
                    self.scaleFactors[sf_name] = ScaleFactor(sf_file[0], sf_file[1])
                else:
                    self.scaleFactors[sf_name] = ScaleFactor(sf_file)

        self.dataEffs = {}
        self.cfg_ana.dataEffFiles = getattr(self.cfg_ana, 'dataEffFiles', {})
        for sf_name, sf_file in self.cfg_ana.dataEffFiles.items():
            if isinstance(sf_file, tuple):
                self.dataEffs[sf_name] = ScaleFactor(sf_file[0], sf_file[1])
            else:
                self.dataEffs[sf_name] = ScaleFactor(sf_file)


    def beginLoop(self, setup):
        super(LeptonWeighter, self).beginLoop(setup)
        self.averages.add('weight', Average('weight'))

        for sf_name in self.scaleFactors:
            self.averages.add('weight_'+sf_name, Average('weight_'+sf_name))
            self.averages.add('eff_data_'+sf_name, Average('eff_data_'+sf_name))
            self.averages.add('eff_MC_'+sf_name, Average('eff_MC_'+sf_name))

        for sf_name in self.dataEffs:
            self.averages.add('weight_'+sf_name, Average('weight_'+sf_name))

    def process(self, event):
        self.readCollections(event.input)
        lep = getattr(event, self.leptonName)
        lep.weight = 1.

        for sf_name in self.scaleFactors:
            setattr(lep, 'weight_'+sf_name, 1.)
            setattr(lep, 'eff_data_'+sf_name, 1.)
            setattr(lep, 'eff_MC_'+sf_name, 1.)

        for sf_name in self.dataEffs:
            setattr(lep, 'weight_'+sf_name, 1.)

        if (self.cfg_comp.isMC or self.cfg_comp.isEmbed) and \
           not getattr(self.cfg_ana, 'disable', False) and lep.pt() < 9999.:

            isFake = False
            if hasattr(lep, 'tau') and lep.gen_match in [1,2,3,4,6]:
                isFake = True

            iso = None
            if hasattr(lep, 'muonID'): # muon
                iso = lep.relIsoR(R=0.4, dBetaFactor=0.5)

            if hasattr(lep, 'mvaNonTrigV0'): # electron
                iso = lep.relIsoR(R=0.3, dBetaFactor=0.5)

            # Get scale factors
            for sf_name, sf in self.scaleFactors.items():
                pt = lep.pt()
                eta = lep.eta()
                if hasattr(lep,'electronID'):
                    eta = lep.superCluster().eta() # sc eta used for weights in case of electrons
                dm = lep.decayMode() if hasattr(lep, 'decayMode') else None
                setattr(lep, 'weight_'+sf_name, sf.getScaleFactor(pt, eta, isFake, iso=iso, dm=dm))
                # setattr(lep, 'eff_data_'+sf_name, sf.getEfficiencyData(pt, eta, isFake))
                # setattr(lep, 'eff_mc_'+sf_name, sf.getEfficiencyMC(pt, eta, isFake))

                if sf_name in self.cfg_ana.scaleFactorFiles:
                    lep.weight *= getattr(lep, 'weight_'+sf_name)

            for sf_name, sf in self.dataEffs.items():
                pt = lep.pt()
                eta = lep.eta()
                dm = lep.decayMode() if hasattr(lep, 'decayMode') else None
                setattr(lep, 'weight_'+sf_name, sf.getEfficiencyData(pt, eta, isFake, iso=iso, dm=dm))
                
                if sf_name in self.cfg_ana.dataEffFiles:
                    lep.weight *= getattr(lep, 'weight_'+sf_name,1.)
        
        # no idisoweight ?
        if 'idiso' not in self.scaleFactors and 'idiso' not in self.dataEffs : #if not hasattr(lep,'weight_idiso'):
            lep.weight_idiso = 1.
            if hasattr(lep,'weight_id'):
                lep.weight_idiso *= lep.weight_id
            if hasattr(lep,'weight_iso'):
                lep.weight_idiso *= lep.weight_iso
        
        event.triggerWeight = getattr(event, 'triggerWeight', 1.)

        if 'trigger' in self.scaleFactors:
            event.triggerWeight *= lep.weight_trigger

        if 'trigger' in self.dataEffs:
            event.triggerWeight *= lep.weight_trigger

        event.eventWeight *= lep.weight

        self.averages['weight'].add(lep.weight)
        for sf_name in self.scaleFactors:
            self.averages['weight_'+sf_name].add(getattr(lep, 'weight_'+sf_name))
            self.averages['eff_data_'+sf_name].add(getattr(lep, 'eff_data_'+sf_name))
            self.averages['eff_MC_'+sf_name].add(getattr(lep, 'eff_MC_'+sf_name))

        for sf_name in self.dataEffs:
            self.averages['weight_'+sf_name].add(getattr(lep, 'weight_'+sf_name))
        

