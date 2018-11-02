from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

class MuTauFakeReweighter(Analyzer):
    '''Reweight muon->tauh fakes as derived here:
    https://indico.cern.ch/event/715039/contributions/2939095/attachments/1619524/2575700/leptauFRRereco_20180319.pdf slide 8
    '''

    @staticmethod
    def sfTight(eta):
        eta = abs(eta)
        if eta < 0.4:
            return 1.17
        if eta < 0.8:
            return 1.29
        if eta < 1.2:
            return 1.14
        if eta < 1.7:
            return 0.93
        if eta < 2.3:
            return 1.61

        print 'MuTauFakeReweighter: invalid eta', eta, 'returning SF of 1'
        return 1.

    @staticmethod
    def sfLoose(eta):
        eta = abs(eta)
        if eta < 0.4:
            return 1.06
        if eta < 0.8:
            return 1.02
        if eta < 1.2:
            return 1.10
        if eta < 1.7:
            return 1.03
        if eta < 2.3:
            return 1.94

        print 'MuTauFakeReweighter: invalid eta', eta, 'returning SF of 1'
        return 1.

    def process(self, event):
        event.zllWeight = 1
        if not self.cfg_comp.isMC:
            return True

        # Only apply corrections for leptons giving rise to fake hadronic taus
        if event.leg2.gen_match not in [2, 4]:
            return True

        tau = event.diLepton.leg2()
        
        if self.cfg_ana.wp == 'tight':
            event.zllWeight = self.sfTight(tau.eta())
        elif self.cfg_ana.wp == 'loose':
            event.zllWeight = self.sfLoose(tau.eta())
        else:
            print 'MuTauFakeReweighter: invalid working point', self.cfg_ana.wp
        
        if self.cfg_ana.verbose:    
            print 'MuTauFakeReweighter', tau.eta(), event.zllWeight
        
        setattr(event,'MuTauFakeRateSF',event.zllWeight)

        event.eventWeight = event.eventWeight * event.zllWeight
        return True
