from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.physicsobjects.Tau import Tau

from PhysicsTools.HeppyCore.utils.deltar import deltaR, bestMatch
from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

def daughters(p):
    ds = []
    for i_d in xrange(p.numberOfDaughters()):
        ds.append(p.daughter(i_d))
    return ds

class TauIsoAnalyzer(Analyzer):

    '''Gets tau decay mode efficiency weight and puts it in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauIsoAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def declareHandles(self):
        super(TauIsoAnalyzer, self).declareHandles()

        self.handles['taus'] = AutoHandle('slimmedTaus', 'std::vector<pat::Tau>')
        self.handles['pu'] = AutoHandle('slimmedAddPileupInfo', 'std::vector<PileupSummaryInfo>')
        self.handles['gen'] = AutoHandle('prunedGenParticles', 'std::vector<reco::GenParticle>')
        self.handles['gen_jets'] = AutoHandle('slimmedGenJets', 'vector<reco::GenJet>>')
        self.handles['pf_candidates'] = AutoHandle('packedPFCandidates', 'vector<pat::PackedCandidate>>')


    def beginLoop(self, setup):
        print self, self.__class__
        super(TauIsoAnalyzer, self).beginLoop(setup)

    def process(self, event):
        self.readCollections(event.input)

        event.taus = [Tau(tau) for tau in self.handles['taus'].product()]
        event.gen = self.handles['gen'].product()
        event.genParticles = event.gen
        event.genJets = self.handles['gen_jets'].product()

        for pu_info in self.handles['pu'].product():
            if pu_info.getBunchCrossing() == 0:
                event.n_true_interactions = pu_info.getTrueNumInteractions()

        event.genleps = [p for p in event.gen if abs(p.pdgId()) in [11, 13] and p.statusFlags().isPrompt()]
        event.gentauleps = [p for p in event.gen if abs(p.pdgId()) in [11, 13] and p.statusFlags().isDirectPromptTauDecayProduct()]
        event.gentaus = [p for p in event.gen if abs(p.pdgId()) == 15 and p.statusFlags().isPrompt() and not any(abs(HTTGenAnalyzer.getFinalTau(p).daughter(i_d).pdgId()) in [11, 13] for i_d in xrange(HTTGenAnalyzer.getFinalTau(p).numberOfDaughters()))]

        HTTGenAnalyzer.getGenTauJets(event) # saves event.genTauJets

        for gen_tau in event.genTauJets:
            gen_tau.charged = [d for d in gen_tau.daughters if d.charge()]
            gen_tau.pizeros = [daughters(d) for d in gen_tau.daughters if d.pdgId() == 111]

        pf_candidates = self.handles['pf_candidates'].product()

        for tau in event.taus:
            TauIsoAnalyzer.addInfo(tau, event, [c for c in pf_candidates if abs(c.pdgId()) == 211], maxDeltaR=0.8)
            matched_gen_jet, dr2 = bestMatch(tau, event.genJets)
            if dr2 < 0.25:
                tau.gen_jet = matched_gen_jet

        return True

    @staticmethod
    def addInfo(tau, event, cands=None, maxDeltaR=None):
        HTTGenAnalyzer.genMatch(event, tau, event.gentauleps, event.genleps, [], dR=0.2, matchAll=True)
        HTTGenAnalyzer.attachGenStatusFlag(tau)
        TauIsoAnalyzer.tauIsoBreakdown(tau, cands, maxDeltaR=maxDeltaR)
        tau.nphotons = sum(1 for cand in TauIsoAnalyzer.tauFilteredPhotons(tau))

    @staticmethod
    def tauChargedFilteredIso(tau, minDeltaZ=-1., maxDeltaZ=0.2, maxTrackChi2=100., maxTransverseImpactParameter=0.03, minTrackHits=3, minTrackPt=0.5, cands=None, maxDeltaR=None):
        if not cands:
            cands = [cand.get() for cand in tau.isolationChargedHadrCands()]
        pv = tau.vertex()
        filteredCands = []
        for cand in cands:
            if maxDeltaR:
                # Speed up
                if abs(cand.eta() - tau.eta()) > maxDeltaR or abs(cand.phi() - tau.phi()) > maxDeltaR:
                    continue
                if deltaR(tau, cand) > maxDeltaR:
                    continue

            track = cand.bestTrack()
            if not track:
                continue
            
            if TauIsoAnalyzer.filterTrack(track, pv, minDeltaZ, maxDeltaZ, maxTrackChi2, maxTransverseImpactParameter, minTrackHits, minTrackPt):
                continue

            filteredCands.append(cand)
        return filteredCands

    @staticmethod
    def filterTrack(track, pv, minDeltaZ=-1., maxDeltaZ=0.2, maxTrackChi2=100., maxTransverseImpactParameter=0.03, minTrackHits=3, minTrackPt=0.5):
        return (track.pt() < minTrackPt
                or track.normalizedChi2() > maxTrackChi2
                or track.hitPattern().numberOfValidHits() < minTrackHits
                or abs(track.dz(pv)) > maxDeltaZ
                or abs(track.dz(pv)) < minDeltaZ
                or abs(track.dxy(pv)) > maxTransverseImpactParameter)

    @staticmethod
    def tauPhotonsOutsideSignalCone(tau):
        filteredCands = []
        # signalConeSize = tau.signalConeSize()
        signalConeSize = max(min(0.1, 3.0/tau.pt()), 0.05)
        for c in tau.signalGammaCands():
            if deltaR(tau, c) > signalConeSize:
                filteredCands.append(c)
        return filteredCands

    @staticmethod
    def tauFilteredPhotons(tau, minPt=0.5, maxDR=0.5):
        filteredCands = []
        for cand in tau.isolationGammaCands():
            if (cand.pt() < minPt
                or deltaR(cand, tau) > maxDR):
                continue
            filteredCands.append(cand)
        return filteredCands

    @staticmethod
    def tauIsoBreakdown(tau, pf_candidates=None, maxDeltaR=None):
        # calculate photon pT outside signal cone
        variables = {
            'ptSumIso': tau.isolationCands(),
            'chargedPtSumIso': TauIsoAnalyzer.tauChargedFilteredIso(tau),
            'chargedPUPtSumIso': TauIsoAnalyzer.tauChargedFilteredIso(tau, minDeltaZ=0.2, maxDeltaZ=99999., cands=pf_candidates, maxDeltaR=maxDeltaR),
            'gammaPtSumIso': TauIsoAnalyzer.tauFilteredPhotons(tau),
            'gammaPtSumOutsideSignalCone': TauIsoAnalyzer.tauPhotonsOutsideSignalCone(tau),
            'neutralPtSumIso': tau.isolationNeutrHadrCands(),
            'ptSumSignal': tau.signalCands(),
            'chargedCandsPtSumSignal': tau.signalChargedHadrCands(),
            'gammaCandsPtSumSignal': tau.signalGammaCands(),
            'neutralCandsPtSumSignal': tau.signalNeutrHadrCands(),
        }

        for k, v in variables.items():
            ptsum = 0.
            for i in v:
                ptsum += i.pt()
            setattr(tau, k, ptsum)
