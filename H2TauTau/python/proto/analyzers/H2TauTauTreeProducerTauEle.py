import ROOT

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducer import H2TauTauTreeProducer
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

class H2TauTauTreeProducerTauEle(H2TauTauTreeProducer):
    '''Tree producer for the H->tau tau analysis.'''

    def declareVariables(self, setup):

        super(H2TauTauTreeProducerTauEle, self).declareVariables(setup)

        self.bookTau(self.tree, 'l2')
        self.bookEle(self.tree, 'l1')

        self.bookGenParticle(self.tree, 'l2_gen')
        self.var(self.tree, 'l2_gen_lepfromtau', int)
        self.bookGenParticle(self.tree, 'l1_gen')
        self.var(self.tree, 'l1_gen_lepfromtau', int)

        self.bookParticle(self.tree, 'l2_gen_vis')
        self.var(self.tree, 'l2_gen_decaymode', int)

        self.var(self.tree, 'l2_gen_nc_ratio')
        self.var(self.tree, 'l2_nc_ratio')

        self.var(self.tree, 'l2_weight_fakerate')
        self.var(self.tree, 'l2_weight_fakerate_up')
        self.var(self.tree, 'l2_weight_fakerate_down')

        #self.var( self.tree, 'weight_zll')

    def process(self, event):

        super(H2TauTauTreeProducerTauEle, self).process(event)

        tau = event.diLepton.leg2()
        ele = event.diLepton.leg1()

        self.fillTau(self.tree, 'l2', tau)
        self.fillEle(self.tree, 'l1', ele)

        if hasattr(tau, 'genp') and tau.genp:
            self.fillGenParticle(self.tree, 'l2_gen', tau.genp)
            self.fill(self.tree, 'l2_gen_lepfromtau', tau.isTauLep)
        if hasattr(ele, 'genp') and ele.genp:
            self.fillGenParticle(self.tree, 'l1_gen', ele.genp)
            self.fill(self.tree, 'l1_gen_lepfromtau', ele.isTauLep)

        if hasattr(ele, 'triggerobjects'):
            n_triggerobjects = len(ele.triggerobjects)
            self.fill(self.tree, 'l1_ntriggerobjects', n_triggerobjects)
            if n_triggerobjects >= 1:
                self.fillParticle(self.tree, 'l1_triggerobject1', ele.triggerobjects[0])
            if n_triggerobjects >= 2:
                self.fillParticle(self.tree, 'l1_triggerobject2', ele.triggerobjects[1])
        
        # save the p4 of the visible tau products at the generator level
        if tau.genJet() and hasattr(tau, 'genp') and tau.genp and abs(tau.genp.pdgId()) == 15:
            self.fillParticle(self.tree, 'l2_gen_vis', tau.physObj.genJet())
            tau_gen_dm = tauDecayModes.translateGenModeToInt(tauDecayModes.genDecayModeFromGenJet(tau.physObj.genJet()))
            self.fill(self.tree, 'l2_gen_decaymode', tau_gen_dm)
            if tau_gen_dm in [1, 2, 3, 4]:
                pt_neutral = 0.
                pt_charged = 0.
                for daughter in tau.genJet().daughterPtrVector():
                    id = abs(daughter.pdgId())
                    if id in [22, 11]:
                        pt_neutral += daughter.pt()
                    elif id not in [11, 13, 22] and daughter.charge():
                        if daughter.pt() > pt_charged:
                            pt_charged = daughter.pt()
                if pt_charged > 0.:
                    self.fill(self.tree, 'l2_gen_nc_ratio', (pt_charged - pt_neutral)/(pt_charged + pt_neutral))

        if tau.decayMode() in [1, 2, 3, 4]:
            pt_neutral = 0.
            pt_charged = 0.
            # for cand_ptr in tau.signalCands(): # THIS CRASHES
            for i_cand in xrange(len(tau.signalCands())):
                cand = tau.signalCands()[i_cand]
                id = abs(cand.pdgId())
                if id in [11, 22, 130]:
                    pt_neutral += cand.pt()
                elif id in [211]:
                    if cand.pt() > pt_charged:
                        pt_charged = cand.pt()
            if pt_charged > 0.:
                self.fill(self.tree, 'l2_nc_ratio', (pt_charged - pt_neutral)/(pt_charged + pt_neutral))

        self.fill(self.tree, 'l2_weight_fakerate', event.tauFakeRateWeight )
        self.fill(self.tree, 'l2_weight_fakerate_up', event.tauFakeRateWeightUp)
        self.fill(self.tree, 'l2_weight_fakerate_down', event.tauFakeRateWeightDown)

        fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]

        if hasattr(self.cfg_ana, 'addTauTrackInfo') and self.cfg_ana.addTauTrackInfo:
            # Leading CH part
            if tau.signalChargedHadrCands().size() == 0:
                print 'Uh, tau w/o charged hadron???'
            
            leading_ch = tau.signalChargedHadrCands()[0].get()
            self.fillTrackInfo(leading_ch, 'tau_lead_ch')

            # Iso part
            i_lead_ch = -1
            n_ch = len(tau.isolationChargedHadrCands())
            n_gamma = len(tau.isolationGammaCands())

            self.fill(self.tree, 'tau_iso_n_ch', n_ch)
            self.fill(self.tree, 'tau_iso_n_gamma', n_gamma)

            for i_cand in xrange(n_ch):
                if i_lead_ch >= 0:
                    if tau.isolationChargedHadrCands()[i_cand].get().pt() > tau.isolationChargedHadrCands()[i_lead_ch].get().pt():
                        i_lead_ch = i_cand
                else:
                    i_lead_ch = i_cand

            if i_lead_ch >= 0 and tau.isolationChargedHadrCands()[i_lead_ch].get().pt() > 0.95:
                track = tau.isolationChargedHadrCands()[i_lead_ch].get()
                self.fillTrackInfo(track, 'tau_leadiso_ch')

        #self.fill(self.tree, 'weight_zll', event.zllWeight)

        self.fillTree(event)
