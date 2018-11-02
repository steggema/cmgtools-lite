import ROOT

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducer import H2TauTauTreeProducer
from CMGTools.H2TauTau.proto.analyzers.tau_utils import n_photons_tau, e_over_h, tau_pt_weighted_dr_iso, tau_pt_weighted_dphi_strip, tau_pt_weighted_deta_strip, tau_pt_weighted_dr_signal
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

class H2TauTauTreeProducerTauMu(H2TauTauTreeProducer):

    '''Tree producer for the H->tau tau analysis.'''

    def declareVariables(self, setup):

        super(H2TauTauTreeProducerTauMu, self).declareVariables(setup)

        self.bookTau(self.tree, 'l2')
        self.bookMuon(self.tree, 'l1')

        # TODO add triggers in H2tautauproducer
        # self.var(self.tree, 'trigger_isomu24')
        # self.var(self.tree, 'trigger_isomu27')

        # self.var(self.tree, 'trigger_matched_isomu24')
        # self.var(self.tree, 'trigger_matched_isomu27')

        # self.var(self.tree, 'trigger_matched_singlemuon')


        if getattr(self.cfg_ana, 'addTauMVAInputs', False):
            self.var(self.tree, 'l2_n_photons')
            self.var(self.tree, 'l2_e_over_h')
            self.var(self.tree, 'l2_pt_weighted_dr_iso')
            self.var(self.tree, 'l2_pt_weighted_dr_signal')
            self.var(self.tree, 'l2_pt_weighted_dphi_strip')
            self.var(self.tree, 'l2_pt_weighted_deta_strip')

            self.var(self.tree, 'l2_flightLength')
            self.var(self.tree, 'l2_flightLengthSig')
            self.var(self.tree, 'l2_dxy_Sig')
            self.var(self.tree, 'l2_ip3d')
            self.var(self.tree, 'l2_ip3d_error')
            self.var(self.tree, 'l2_ip3d_Sig')
            self.var(self.tree, 'l2_leadingTrackNormChi2')
            self.var(self.tree, 'l2_leadingTrackNormChi2')

        if getattr(self.cfg_ana, 'addIsoInfo', False):

            self.var(self.tree, 'l1_puppi_iso_pt')
            self.var(self.tree, 'l1_puppi_iso04_pt')
            self.var(self.tree, 'l1_puppi_iso03_pt')

            self.var(self.tree, 'l1_puppi_no_muon_iso_pt')
            self.var(self.tree, 'l1_puppi_no_muon_iso04_pt')
            self.var(self.tree, 'l1_puppi_no_muon_iso03_pt')

            self.var(self.tree, 'l2_puppi_iso_pt')
            self.var(self.tree, 'l2_puppi_iso04_pt')
            self.var(self.tree, 'l2_puppi_iso03_pt')

            self.var(self.tree, 'l1_mini_iso')
            self.var(self.tree, 'l1_mini_reliso')

        if getattr(self.cfg_ana, 'addTauTrackInfo', False):
            self.var(self.tree, 'tau_iso_n_ch')
            self.var(self.tree, 'tau_iso_n_gamma')
            self.bookTrackInfo('tau_lead_ch')
            self.bookTrackInfo('tau_leadiso_ch')

        if getattr(self.cfg_ana, 'addTnPInfo', False):
            self.var(self.tree, 'tag')
            self.var(self.tree, 'probe')
            self.bookParticle(self.tree, 'l1_trig_obj')
            self.bookParticle(self.tree, 'l2_trig_obj')
            self.bookParticle(self.tree, 'l1_L1')
            self.bookParticle(self.tree, 'l2_L1')
            self.var(self.tree, 'l1_L1_type')
            self.var(self.tree, 'l2_L1_type')
            # RM add further branches related to the HLT filter matching by hand.
            #    I cannot find a better solution for the moment 14/10/2015
            self.bookParticle(self.tree, 'l2_hltL2Tau30eta2p2')


    def bookTrackInfo(self, name):
        self.var(self.tree, name + '_pt')
        self.var(self.tree, name + '_dxy')
        self.var(self.tree, name + '_dz')
        self.var(self.tree, name + '_ndof')
        self.var(self.tree, name + '_chi2')
        self.var(self.tree, name + '_normchi2')
        self.var(self.tree, name + '_n_layers_pixel')
        self.var(self.tree, name + '_n_hits_pixel')
        self.var(self.tree, name + '_n_layers_tracker')
        self.var(self.tree, name + '_n_hits')
        self.var(self.tree, name + '_n_missing_inner')
        self.var(self.tree, name + '_high_purity')

    def fillTrackInfo(self, track, name='tau_track'):
        pt = track.pt()
        ndof = track.pseudoTrack().ndof()
        dxy = track.dxy()
        dz = track.dz()
        chi2 = track.pseudoTrack().chi2()
        norm_chi2 = track.pseudoTrack().normalizedChi2()

        n_layers_pixel = track.pseudoTrack().hitPattern().pixelLayersWithMeasurement()
        n_hits_pixel = track.numberOfPixelHits()
        n_layers_tracker = track.pseudoTrack().hitPattern().trackerLayersWithMeasurement()
        n_hits = track.numberOfHits()
        n_missing_inner = track.lostInnerHits()
        high_purity = track.pseudoTrack().quality(ROOT.reco.TrackBase.highPurity)

        self.fill(self.tree, name + '_pt', pt)
        self.fill(self.tree, name + '_dxy', dxy)
        self.fill(self.tree, name + '_dz', dz)
        self.fill(self.tree, name + '_ndof', ndof)
        self.fill(self.tree, name + '_chi2', chi2)
        self.fill(self.tree, name + '_normchi2', norm_chi2)
        self.fill(self.tree, name + '_n_layers_pixel', n_layers_pixel)
        self.fill(self.tree, name + '_n_hits_pixel', n_hits_pixel)
        self.fill(self.tree, name + '_n_layers_tracker', n_layers_tracker)
        self.fill(self.tree, name + '_n_hits', n_hits)
        self.fill(self.tree, name + '_n_missing_inner', n_missing_inner)
        self.fill(self.tree, name + '_high_purity', high_purity)

    def process(self, event):

        super(H2TauTauTreeProducerTauMu, self).process(event)

        tau = event.diLepton.leg2()
        muon = event.diLepton.leg1()
       
        self.fillTau(self.tree, 'l2', tau)
        self.fillMuon(self.tree, 'l1', muon)


        # TODO add triggers in H2tautauproducer
        # fired_triggers = [info.name for info in getattr(event, 'trigger_infos', []) if info.fired]

        # self.fill(self.tree, 'trigger_isomu24', any('IsoMu24_v' in name for name in fired_triggers))
        # self.fill(self.tree, 'trigger_isomu27', any('IsoMu27_v' in name for name in fired_triggers))

        # matched_paths = getattr(event.diLepton, 'matchedPaths', [])
        # self.fill(self.tree, 'trigger_matched_isomu24', any('IsoMu24_v' in name for name in matched_paths))
        # self.fill(self.tree, 'trigger_matched_isomu27', any('IsoMu27_v' in name for name in matched_paths))

        # self.fill(self.tree, 'trigger_matched_singlemuon', any('Mu22' in name for name in matched_paths))





        ### Start of conditionnal vars

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


        if hasattr(self.cfg_ana, 'addIsoInfo') and self.cfg_ana.addIsoInfo:
            self.fill(self.tree, 'l1_puppi_iso_pt', muon.puppi_iso_pt)
            self.fill(self.tree, 'l1_puppi_iso04_pt', muon.puppi_iso04_pt)
            self.fill(self.tree, 'l1_puppi_iso03_pt', muon.puppi_iso03_pt)
            self.fill(self.tree, 'l1_puppi_no_muon_iso_pt', muon.puppi_no_muon_iso_pt)
            self.fill(self.tree, 'l1_puppi_no_muon_iso04_pt', muon.puppi_no_muon_iso04_pt)
            self.fill(self.tree, 'l1_puppi_no_muon_iso03_pt', muon.puppi_no_muon_iso03_pt)
            self.fill(self.tree, 'l2_puppi_iso_pt', tau.puppi_iso_pt)
            self.fill(self.tree, 'l2_puppi_iso04_pt', tau.puppi_iso04_pt)
            self.fill(self.tree, 'l2_puppi_iso03_pt', tau.puppi_iso03_pt)
            self.fill(self.tree, 'l1_mini_iso', muon.miniAbsIso)
            self.fill(self.tree, 'l1_mini_reliso', muon.miniRelIso)

        if hasattr(self.cfg_ana, 'addTnPInfo') and self.cfg_ana.addTnPInfo:
            self.fill(self.tree, 'tag', event.tag)
            self.fill(self.tree, 'probe', event.probe)
            if hasattr(muon, 'to'):
                self.fillParticle(self.tree, 'l1_trig_obj', muon.to)
            if hasattr(tau, 'to'):            
                self.fillParticle(self.tree, 'l2_trig_obj', tau.to)
            if hasattr(muon, 'L1'):
                self.fillParticle(self.tree, 'l1_L1', muon.L1)
                self.fill(self.tree, 'l1_L1_type', muon.L1flavour)
            if hasattr(tau, 'L1'):
                self.fillParticle(self.tree, 'l2_L1', tau.L1)
                self.fill(self.tree, 'l2_L1_type', tau.L1flavour)
            # RM add further branches related to the HLT filter matching by hand.
            #    I cannot find a better solution for the moment 14/10/2015
            if hasattr(tau, 'hltL2Tau30eta2p2'):
                self.fillParticle(self.tree, 'l2_hltL2Tau30eta2p2', tau.hltL2Tau30eta2p2)

        if getattr(self.cfg_ana, 'addTauMVAInputs', False):
            self.fill(self.tree, 'l2_n_photons', n_photons_tau(tau))
            self.fill(self.tree, 'l2_e_over_h', e_over_h(tau))
            self.fill(self.tree, 'l2_pt_weighted_dr_iso', tau_pt_weighted_dr_iso(tau))
            self.fill(self.tree, 'l2_pt_weighted_dr_signal', tau_pt_weighted_dr_signal(tau))
            self.fill(self.tree, 'l2_pt_weighted_dphi_strip', tau_pt_weighted_dphi_strip(tau))
            self.fill(self.tree, 'l2_pt_weighted_deta_strip', tau_pt_weighted_deta_strip(tau))

            self.fill(self.tree, 'l2_flightLength', tau.flightLength().r())
            self.fill(self.tree, 'l2_flightLengthSig', tau.flightLengthSig())
            self.fill(self.tree, 'l2_dxy_Sig', tau.dxy_Sig())
            self.fill(self.tree, 'l2_ip3d', tau.ip3d())
            self.fill(self.tree, 'l2_ip3d_error', tau.ip3d_error())
            self.fill(self.tree, 'l2_ip3d_Sig', tau.ip3d_Sig())
            self.fill(self.tree, 'l2_leadingTrackNormChi2', tau.leadingTrackNormChi2())
            self.fill(self.tree, 'l2_leadingTrackNormChi2', tau.leadingTrackNormChi2())

            

        self.fillTree(event)
        #import pdb; pdb.set_trace() # weight lt test
