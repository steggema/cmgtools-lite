from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase
from CMGTools.H2TauTau.proto.analyzers.tau_utils import n_photons_tau, e_over_h, tau_pt_weighted_dr_iso, tau_pt_weighted_dphi_strip, tau_pt_weighted_deta_strip, tau_pt_weighted_dr_signal


class TauIsoTreeProducer(H2TauTauTreeProducerBase):
    ''' Tree producer for tau POG study.
    '''

    def __init__(self, *args):
        super(TauIsoTreeProducer, self).__init__(*args)

    def declareHandles(self):
        super(TauIsoTreeProducer, self).declareHandles()


    def declareVariables(self, setup):

        self.bookTau(self.tree, 'tau')
        self.bookParticle(self.tree, 'gen_jet')
        self.bookParticle(self.tree, 'gen_vis_tau')

        self.tree.var('n_true_interactions')

        self.tree.var('tau_z')
        self.tree.var('tau_n_photons')
        self.tree.var('tau_e_over_h')
        self.tree.var('tau_pt_weighted_dr_iso')
        self.tree.var('tau_pt_weighted_dr_signal')
        self.tree.var('tau_pt_weighted_dphi_strip')
        self.tree.var('tau_pt_weighted_deta_strip')

        self.tree.var('tau_flightLength')
        self.tree.var('tau_flightLengthSig')
        self.tree.var('tau_dxy_Sig')
        self.tree.var('tau_ip3d')
        self.tree.var('tau_ip3d_error')
        self.tree.var('tau_ip3d_Sig')
        self.tree.var('tau_leadingTrackNormChi2')
        self.tree.var('tau_leadingTrackNormChi2')

        self.tree.var('tau_n_iso_ch', type=int, default=0)
        self.tree.vector('tau_iso_ch_dz', 'tau_n_iso_ch', maxlen=99, type=float)
        self.tree.vector('tau_iso_ch_dxy', 'tau_n_iso_ch', maxlen=99, type=float)
        self.tree.vector('tau_iso_ch_pt', 'tau_n_iso_ch', maxlen=99, type=float)
        self.tree.vector('tau_iso_ch_dr', 'tau_n_iso_ch', maxlen=99, type=float)

        self.tree.var('tau_n_iso_ph', type=int, default=0)
        self.tree.vector('tau_iso_ph_pt', 'tau_n_iso_ph', maxlen=99, type=float)
        self.tree.vector('tau_iso_ph_dr', 'tau_n_iso_ph', maxlen=99, type=float)

        self.tree.var('tau_ptSumIso_recalc')
        self.tree.var('tau_chargedIsoPtSum_recalc')
        self.tree.var('tau_puCorrPtSum_recalc')
        self.tree.var('tau_neutralIsoPtSum_recalc')
        self.tree.var('tau_photonPtSumOutsideSignalCone_recalc')
        self.tree.var('tau_neutralHadronIsoPtSum_recalc')
        self.tree.var('tau_ptSumSignal_recalc')
        self.tree.var('tau_chargedCandsPtSumSignal_recalc')
        self.tree.var('tau_gammaCandsPtSumSignal_recalc')
        self.tree.var('tau_neutralCandsPtSumSignal_recalc')


    def process(self, event):
        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.readCollections(event.input)

        if not eval(self.skimFunction):
            return False
        
        tau_gen_jet_gen_tau_triplets = []
        matched_gen_jets = []
        matched_gen_taus = []

        for tau in event.taus:
            if getattr(tau, 'gen_jet', None):
                if tau.isTauHad:
                    tau_gen_jet_gen_tau_triplets.append((tau, tau.gen_jet, tau.genp))
                    matched_gen_taus.append(tau.genp)
                else:
                    tau_gen_jet_gen_tau_triplets.append((tau, tau.gen_jet, None))
                matched_gen_jets.append(tau.gen_jet)
            else:
                if tau.isTauHad:
                    tau_gen_jet_pairs.append((tau, None, tau.genp))
                    matched_gen_taus.append(tau.genp)
                else:
                    tau_gen_jet_gen_tau_triplets.append((tau, None, None))
        
        other_gen_jets = [j for j in event.genJets if j.pt() > 18. and abs(j.eta()) < 2.3 and j not in matched_gen_jets]
        other_gen_taus = [t for t in event.genTauJets if t.pt() > 18. and abs(t.eta()) < 2.3 and t not in matched_gen_taus]
        
        if any(deltaR(tau, gen_jet) < 0.09 for tau in event.taus for gen_jet in other_gen_jets):
            print 'Warning: found generator jet close to tau that was not cleaned'

        if any(deltaR(tau, gen_tau) < 0.09 for tau in event.taus for gen_tau in other_gen_taus):
            print 'Warning: found generator tau close to tau that was not cleaned'


        gj_matched_gen_taus = []

        for gen_jet in other_gen_jets:
            for gvt in other_gen_taus:
                if deltaR2(gen_jet, gvt) < 0.09:
                    tau_gen_jet_gen_tau_triplets.append((None, gen_jet, gvt))
                    gj_matched_gen_taus.append(gvt)
            else:
                tau_gen_jet_gen_tau_triplets.append((None, gen_jet, None))

        other_gen_taus = [t for t in other_gen_taus if t not in gj_matched_gen_taus]

        for gvt in other_gen_taus:
            tau_gen_jet_gen_tau_triplets.append((None, None, gvt))

        for tau, gen_jet, gen_vis_tau in tau_gen_jet_gen_tau_triplets:
            self.tree.reset()
            self.tree.fill('n_true_interactions', event.n_true_interactions)
            
            if gen_vis_tau:
                self.fillParticle(self.tree, 'gen_vis_tau', gen_vis_tau)
            if gen_jet:
                self.fillParticle(self.tree, 'gen_jet', gen_jet)
            if tau:
                self.fillTau(self.tree, 'tau', tau)

                if getattr(self.cfg_ana, 'reject_gen_leptons', False) and tau.gen_match < 5: 
                    continue

                self.tree.fill('tau_z', tau.vertex().z())
                self.tree.fill('tau_n_photons', n_photons_tau(tau))
                self.tree.fill('tau_e_over_h', e_over_h(tau))
                self.tree.fill('tau_pt_weighted_dr_iso', tau_pt_weighted_dr_iso(tau))
                self.tree.fill('tau_pt_weighted_dr_signal', tau_pt_weighted_dr_signal(tau))
                self.tree.fill('tau_pt_weighted_dphi_strip', tau_pt_weighted_dphi_strip(tau))
                self.tree.fill('tau_pt_weighted_deta_strip', tau_pt_weighted_deta_strip(tau))

                self.tree.fill('tau_flightLength', tau.flightLength().r())
                self.tree.fill('tau_flightLengthSig', tau.flightLengthSig())
                self.tree.fill('tau_dxy_Sig', tau.dxy_Sig())
                self.tree.fill('tau_ip3d', tau.ip3d())
                self.tree.fill('tau_ip3d_error', tau.ip3d_error())
                self.tree.fill('tau_ip3d_Sig', tau.ip3d_Sig())
                self.tree.fill('tau_leadingTrackNormChi2', tau.leadingTrackNormChi2())

                self.tree.fill('tau_n_iso_ch', tau.isolationChargedHadrCands().size())
                dzs = []
                dxys = []
                pts = []
                drs = []
                for iso_ch in tau.isolationChargedHadrCands():
                    dzs.append(iso_ch.dz(tau.vertex()))
                    dxys.append(iso_ch.dxy(tau.vertex()))
                    pts.append(iso_ch.pt())
                    drs.append(deltaR(iso_ch, tau))
                self.tree.vfill('tau_iso_ch_dz', dzs)
                self.tree.vfill('tau_iso_ch_dxy', dxys)
                self.tree.vfill('tau_iso_ch_pt', pts)
                self.tree.vfill('tau_iso_ch_dr', drs)

                self.tree.fill('tau_n_iso_ph', tau.isolationGammaCands().size())
                pts = []
                drs = []
                for iso_ph in tau.isolationGammaCands():
                    pts.append(iso_ph.pt())
                    drs.append(deltaR(iso_ph, tau))
                self.tree.vfill('tau_iso_ph_pt', pts)
                self.tree.vfill('tau_iso_ph_dr', drs)

                self.tree.fill('tau_ptSumIso_recalc', tau.ptSumIso)
                self.tree.fill('tau_chargedIsoPtSum_recalc', tau.chargedPtSumIso)
                self.tree.fill('tau_puCorrPtSum_recalc', tau.chargedPUPtSumIso)
                self.tree.fill('tau_neutralIsoPtSum_recalc', tau.gammaPtSumIso)
                self.tree.fill('tau_photonPtSumOutsideSignalCone_recalc', tau.gammaPtSumOutsideSignalCone)
                self.tree.fill('tau_neutralHadronIsoPtSum_recalc', tau.neutralPtSumIso)
                self.tree.fill('tau_ptSumSignal_recalc', tau.ptSumSignal)
                self.tree.fill('tau_chargedCandsPtSumSignal_recalc', tau.chargedCandsPtSumSignal)
                self.tree.fill('tau_gammaCandsPtSumSignal_recalc', tau.gammaCandsPtSumSignal)
                self.tree.fill('tau_neutralCandsPtSumSignal_recalc', tau.neutralCandsPtSumSignal)

            self.fillTree(event)
