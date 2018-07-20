import ROOT
import copy

from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon import Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Tau import Tau

from CMGTools.H2TauTau.proto.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer
from CMGTools.H2TauTau.proto.physicsobjects.DiObject import TauMuon, DirectDiTau
from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

from PhysicsTools.HeppyCore.utils.deltar import deltaR

class TauMuAnalyzer(DiLeptonAnalyzer):

    DiObjectClass = TauMuon
    LeptonClass = Muon
    OtherLeptonClass = Electron

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauMuAnalyzer,self).__init__(cfg_ana, cfg_comp, looperName)
        import os.path
        

    def declareHandles(self):
        super(TauMuAnalyzer, self).declareHandles()

        if hasattr(self.cfg_ana, 'from_single_objects') and self.cfg_ana.from_single_objects:
            self.handles['taus'] = AutoHandle(
                'slimmedTaus',
                'std::vector<pat::Tau>'
            )
        else:
            self.handles['diLeptons'] = AutoHandle(
                'cmgTauMuCorSVFitFullSel',
                'std::vector<pat::CompositeCandidate>'
            )

        self.handles['otherLeptons'] = AutoHandle(
            'slimmedElectrons',
            'std::vector<pat::Electron>'
        )

        self.handles['leptons'] = AutoHandle(
            'slimmedMuons',
            'std::vector<pat::Muon>'
        )

        self.mchandles['genParticles'] = AutoHandle(
            'prunedGenParticles',
            'std::vector<reco::GenParticle>'
        )


    def buildDiLeptons(self, patDiLeptons, event):
        '''Build di-leptons, associate best vertex to both legs,
        select di-leptons with a tight ID muon.
        The tight ID selection is done so that dxy and dz can be computed
        (the muon must not be standalone).
        '''
        diLeptons = []
        for index, dil in enumerate(patDiLeptons):
            #pydil = self.__class__.DiObjectClass(dil)
            pydil = TauMuon(dil)
            pydil.leg2().associatedVertex = event.goodVertices[0]
            pydil.leg1().associatedVertex = event.goodVertices[0]
            pydil.leg1().event = event.input.object()
            pydil.leg2().event = event.input.object()
            if not self.testLeg1(pydil.leg1(), 99999):
                continue
            # JAN: This crashes. Waiting for idea how to fix this; may have
            # to change data format otherwise, though we don't yet strictly
            # need the MET significance matrix here since we calculate SVFit
            # before
            pydil.mvaMetSig = pydil.met().getSignificanceMatrix()
            diLeptons.append(pydil)
        return diLeptons

    def buildDiLeptonsSingle(self, leptons, event):
        di_leptons = []
        met = event.pfmet
        for pat_mu in leptons:
            muon = self.__class__.LeptonClass(pat_mu)
            for pat_tau in self.handles['taus'].product():
                tau = Tau(pat_tau)
                di_tau = DirectDiTau(muon, tau, met)
                di_tau.leg2().associatedVertex = event.goodVertices[0]
                di_tau.leg1().associatedVertex = event.goodVertices[0]
                di_tau.leg1().event = event.input.object()
                di_tau.leg2().event = event.input.object()
                if not self.testLeg1(di_tau.leg1(), 99999):
                    continue

                di_tau.mvaMetSig = None
                di_leptons.append(di_tau)
        return di_leptons

    def buildLeptons(self, patLeptons, event):
        '''Build muons for veto, associate best vertex, select loose ID muons.
        The loose ID selection is done to ensure that the muon has an inner track.'''
        leptons = []
        for index, lep in enumerate(patLeptons):
            pyl = self.__class__.LeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.event = event.input.object()
            leptons.append(pyl)
        return leptons

    def buildOtherLeptons(self, patOtherLeptons, event):
        '''Build electrons for third lepton veto, associate best vertex.
        '''
        otherLeptons = []
        for index, lep in enumerate(patOtherLeptons):
            pyl = self.__class__.OtherLeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.rho = event.rho
            pyl.event = event.input.object()
            otherLeptons.append(pyl)
        return otherLeptons

    def process(self, event):
        # Take the pre-sorted vertices from miniAOD
        event.goodVertices = event.vertices

        super(TauMuAnalyzer, self).process(event)

        result = self.selectionSequence(event, fillCounter=True,
                                        leg1IsoCut=self.cfg_ana.iso1,
                                        leg2IsoCut=self.cfg_ana.iso2)
        return result

    def testLeg2ID(self, tau):
        return (tau.tauID('decayModeFinding') > 0.5 and
                abs(tau.charge()) == 1. and
                self.testTauVertex(tau))
        # https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendation13TeV

    def testLeg2Iso(self, tau, isocut):
        '''if isocut is None, returns true if three-hit iso cut is passed.
        Otherwise, returns true if iso MVA > isocut.'''
        return tau.mva_passes('Eff95') 

    def testTauVertex(self, tau):
        '''Tests vertex constraints, for tau'''
        # Just checks if the primary vertex the tau was reconstructed with
        # corresponds to the one used in the analysis
        # isPV = abs(tau.vertex().z() - tau.associatedVertex.z()) < 0.2
        isPV = abs(tau.leadChargedHadrCand().dz()) < 0.2
        return isPV

    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu'''
        return abs(lepton.dxy()) < 0.045 and abs(lepton.dz()) < 0.2

    def testLeg1ID(self, muon):
        '''Tight muon selection, no isolation requirement'''
        return muon.muonID("POG_ID_Medium") and self.testVertex(muon)

    def testLeg1Iso(self, muon, isocut):
        '''Tight muon selection, with isolation requirement'''
        if isocut is None:
            return True # No isolation cut
        else:
            return muon.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=False) < isocut

    def thirdLeptonVeto(self, leptons, otherLeptons, isoCut=0.3):
        # count tight muons
        vLeptons = [muon for muon in leptons if
                    muon.muonID("POG_ID_Medium") and
                    self.testVertex(muon) and
                    self.testLegKine(muon, ptcut=10, etacut=2.4) and
                    self.testLeg1Iso(muon, 0.3)
                    ]

        if len(vLeptons) > 1:
            return False

        return True


    def testElectronID(self, electron):
        return electron.mvaIDRun2("Fall17noIso","wp90")

    def otherLeptonVeto(self, leptons, otherLeptons, isoCut=0.3):
        # count electrons
        vOtherLeptons = [electron for electron in otherLeptons if
                         self.testLegKine(electron, ptcut=10, etacut=2.5) and
                         self.testVertex(electron) and
                         self.testElectronID(electron) and
                         electron.passConversionVeto() and
                         electron.physObj.gsfTrack().hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and
                         electron.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.3]

        if len(vOtherLeptons) > 0:
            return False

        return True

    def leptonAccept(self, leptons, event):
        '''Di-lepton veto: returns false if >= 1 OS same flavour lepton pair,
        e.g. >= 1 OS mu pair in the mu tau channel'''
        looseLeptons = [muon for muon in leptons if
                        self.testLegKine(muon, ptcut=15, etacut=2.4) and
                        muon.isLooseMuon() and
                        self.testVertex(muon) and
                        self.testLeg1Iso(muon, 0.3)
                        ]
        nLeptons = len(looseLeptons)

        if event.leg1 not in looseLeptons: 
            looseLeptons.append(event.leg1) #TODO why ?
        
        # by comparison with TauEleAnalyser.py
        if nLeptons < 2:
            return True
        ##
        
        # if there is an opposite-charge muon pair in the event with muons separated by dR>0.15 and both passing the loose selection
        if any(l.charge() > 0 for l in looseLeptons) and \
           any(l.charge() < 0 for l in looseLeptons):
            looseLeptons_positives = [l for l in looseLeptons if l.charge() > 0]
            looseLeptons_negatives = [l for l in looseLeptons if l.charge() < 0]
            for l_pos in looseLeptons_positives :
                for l_neg in looseLeptons_negatives :
                    dR = deltaR(l_pos.eta(), l_pos.phi(),
                                l_neg.eta(), l_neg.phi())
                    if dR>0.15 :
                        return False

        return True

    def trigMatched(self, event, diL, requireAllMatched=False):
        
        matched = super(TauMuAnalyzer, self).trigMatched(event, diL, requireAllMatched=requireAllMatched, ptMin=18.)

        if matched and len(diL.matchedPaths) == 1 and diL.leg1().pt() < 25. and 'IsoMu24' in list(diL.matchedPaths)[0]:
            matched = False

        return matched

    def bestDiLepton(self, diLeptons):
        '''Returns the best diLepton (1st precedence opposite-sign, 2nd precedence
        highest pt1 + pt2).'''

        if len(diLeptons) == 1:
            return diLeptons[0]

        least_iso_highest_pt = lambda dl: (dl.leg1().relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0), -dl.leg1().pt(), -dl.leg2().tauID("byIsolationMVArun2v1DBoldDMwLTraw"), -dl.leg2().pt())

        return sorted(diLeptons, key=lambda dil : least_iso_highest_pt(dil))[0]


    def scaleMet(self, event, diLep):
       
        pfmet = event.pfmet
        puppimet = event.pfmet
        met = diLep.met()

        taus =[diLep.leg2()]

        for tau in taus:
            if not hasattr(tau, 'deltaMet'):
                # tau wasn't scaled
                continue
            pfmetP4    = pfmet.p4()
            puppimetP4 = puppimet.p4()
            metP4      = met.p4()
            # remove pre-calibrated tau from met computation
            pfmetP4    += tau.deltaMet
            puppimetP4 += tau.deltaMet
            metP4      += tau.deltaMet
        
            pfmet.setP4(pfmetP4)
            puppimet.setP4(puppimetP4)
            met.setP4(metP4)
                    
        return True

    def TauEnergyScale(self, diLeptons, event):
        # get genmatch-needed informations, needs to be done in this analyzer to scale, though information is usually gathered afterwards in HTTGenAnalyzer
        genParticles = self.handles['genParticles'].product()

        ptSelGentauleps = [p for p in genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isDirectPromptTauDecayProduct() and p.pt() > 8.]

        ptSelGenleps = [p for p in genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isPrompt() and p.pt() > 8.]

        event.gentaus = [p for p in event.genParticles if abs(p.pdgId()) == 15 and p.statusFlags().isPrompt() and not any(abs(HTTGenAnalyzer.getFinalTau(p).daughter(i_d).pdgId()) in [11, 13] for i_d in xrange(HTTGenAnalyzer.getFinalTau(p).numberOfDaughters()))]

        # create a list of all used leptons without duplicates, using the ROOT.pat::Tau objects as discriminant
        leps = []
        
        for dilep in diLeptons:
            if dilep.leg2().tau not in [lep.tau for lep in leps]:
                leps.append(dilep.leg2())

        # scale leptons
        for lep in leps:
            self.Scale(lep, ptSelGentauleps, ptSelGenleps, event)
            # issue on unscaledP4 for same taus being in two different legs
            for dilep in diLeptons:
                if dilep.leg2().tau == lep.tau:
                    dilep.leg2().unscaledP4 = lep.unscaledP4
        

    def Scale(self, tau, ptSelGentauleps, ptSelGenleps, event):
        # this function should take values of scales from a file
        tau.unscaledP4 = copy.deepcopy(tau.p4())
        HTTGenAnalyzer.genMatch(event, tau, ptSelGentauleps, ptSelGenleps, [])
        HTTGenAnalyzer.attachGenStatusFlag(tau)
        if tau.gen_match==5:
            if tau.decayMode() == 0:
                tau.scaleEnergy(0.995)
            elif tau.decayMode() == 1:
                tau.scaleEnergy(1.011)
            elif tau.decayMode() == 10:
                tau.scaleEnergy(1.006)
        elif tau.gen_match==1:
            if tau.decayMode() == 0:
                tau.scaleEnergy(1.024)
            elif tau.decayMode() == 1:
                tau.scaleEnergy(1.076)
