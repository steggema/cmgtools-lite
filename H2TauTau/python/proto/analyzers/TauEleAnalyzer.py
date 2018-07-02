import ROOT
import copy
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon import Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Tau import Tau

from CMGTools.H2TauTau.proto.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer
from CMGTools.H2TauTau.proto.physicsobjects.DiObject import TauElectron, DirectDiTau
from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

from PhysicsTools.HeppyCore.utils.deltar import deltaR

import FWCore.ParameterSet.Config as cms

class TauEleAnalyzer(DiLeptonAnalyzer):

    DiObjectClass = TauElectron
    LeptonClass = Electron
    OtherLeptonClass = Muon

    def declareHandles(self):
        super(TauEleAnalyzer, self).declareHandles()

        if hasattr(self.cfg_ana, 'from_single_objects') and self.cfg_ana.from_single_objects:
            self.handles['taus'] = AutoHandle(
                'slimmedTaus',
                'std::vector<pat::Tau>'
            )
        else:
            self.handles['diLeptons'] = AutoHandle(
                'cmgTauEleCorSVFitFullSel',
                'std::vector<pat::CompositeCandidate>'
            )

        self.handles['otherLeptons'] = AutoHandle(
            'slimmedMuons',
            'std::vector<pat::Muon>'
        )

        self.handles['leptons'] = AutoHandle(
            'slimmedElectrons',
            'std::vector<pat::Electron>'
        )

        self.mchandles['genParticles'] = AutoHandle('prunedGenParticles',
                                                    'std::vector<reco::GenParticle>')

        self.handles['puppiMET'] = AutoHandle(
            'slimmedMETsPuppi',
            'std::vector<pat::MET>'
        )

        self.handles['pfMET'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )
        
        # for tau energy scale !
        if hasattr(self.cfg_ana, 'tauEnergyScale') and self.cfg_ana.tauEnergyScale:
            self.handles['genParticles'] = AutoHandle( 
            'prunedGenParticles', 
            'std::vector<reco::GenParticle'
            )

    def buildDiLeptons(self, cmgDiLeptons, event):
        '''Build di-leptons, associate best vertex to both legs,
        select di-leptons with a tight ID electron.
        The electron ID selection is done so that dxy and dz can be computed
        '''
        diLeptons = []
        for index, dil in enumerate(cmgDiLeptons):
            #pydil = self.__class__.DiObjectClass(dil)
            pydil = TauElectron(dil)
            pydil.leg2().associatedVertex = event.goodVertices[0]
            pydil.leg1().associatedVertex = event.goodVertices[0]
            pydil.leg1().rho = event.rho
            pydil.leg1().event = event.input.object()
            pydil.leg2().event = event.input.object()
            pydil.mvaMetSig = pydil.met().getSignificanceMatrix()
            diLeptons.append(pydil)
        return diLeptons

    def buildDiLeptonsSingle(self, leptons, event):
        di_leptons = []
        met = self.handles['pfMET'].product()[0]
        for pat_ele in leptons:
            ele = self.__class__.LeptonClass(pat_ele)
            for pat_tau in self.handles['taus'].product():
                tau = Tau(pat_tau)
                di_tau = DirectDiTau(ele, tau, met)
                di_tau.leg2().associatedVertex = event.goodVertices[0]
                di_tau.leg1().associatedVertex = event.goodVertices[0]
                di_tau.leg1().event = event.input.object()
                di_tau.leg2().event = event.input.object()
                di_tau.leg1().rho = event.rho

                di_tau.mvaMetSig = None
                di_leptons.append(di_tau)
        return di_leptons

    def buildLeptons(self, cms_leptons, event):
        '''Build electrons for veto, associate best vertex, select loose ID electrons.
        Since the electrons are used for veto, the 0.3 default isolation cut is left there,
        as well as the pt 15 gev cut'''
        leptons = []
        for index, lep in enumerate(cms_leptons):
            pyl = self.__class__.LeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.rho = event.rho
            pyl.event = event.input.object()

            if pyl.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) > 0.3:
                continue

            leptons.append(pyl)
        return leptons

    def testMuonIDLoose(self, muon):
        '''Loose muon ID and kine, no isolation requirement, for lepton veto'''
        return muon.pt() > 15 and \
            abs(muon.eta()) < 2.4 and \
            muon.isGlobalMuon() and \
            muon.isTrackerMuon() and \
            muon.sourcePtr().userFloat('isPFMuon') and \
            abs(muon.dz()) < 0.2
        # self.testVertex( muon )

    def buildOtherLeptons(self, cmgOtherLeptons, event):
        '''Build muons for third lepton veto, associate best vertex.
        '''
        otherLeptons = []
        for index, lep in enumerate(cmgOtherLeptons):
            pyl = self.__class__.OtherLeptonClass(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.event = event.input.object()
            # if not self.testMuonIDLoose(pyl):
            #     continue
            otherLeptons.append(pyl)
        return otherLeptons

    def process(self, event):
        # FIXME - JAN - for current 2015 sync, but shall we really discard
        # the vertex cuts?
        event.goodVertices = event.vertices

        result = super(TauEleAnalyzer, self).process(event)

        event.isSignal = False
        if result:
            event.isSignal = True

        if hasattr(self.cfg_ana, 'tauEnergyScale') and self.cfg_ana.tauEnergyScale and self.cfg_comp.isMC:
            self.TauEnergyScale(event.diLeptons, event)

        # trying to get a dilepton from the control region.
        # it must have well id'ed and trig matched legs,
        # and di-lepton veto must pass
        # i.e. only the iso requirement is relaxed
        result = self.selectionSequence(event, fillCounter=True,
                                        leg2IsoCut=self.cfg_ana.looseiso1,
                                        leg1IsoCut=self.cfg_ana.looseiso2)
        if result is False:
            # really no way to find a suitable di-lepton,
            # even in the control region
            return False

        event.isSignal = event.isSignal and event.leptonAccept and event.thirdLeptonVeto

        event.pfmet = self.handles['pfMET'].product()[0]
        event.puppimet = self.handles['puppiMET'].product()[0]

        if hasattr(event, 'calibratedPfMet'):
            event.pfmet = event.calibratedPfMet
        else:
            event.pfmet = self.handles['pfMET'].product()[0]

        if hasattr(self.cfg_ana, 'tauEnergyScale') and \
                self.cfg_ana.tauEnergyScale and self.cfg_comp.isMC:
            # correct pfmet for selected taus (only leg2) scaling
            for lep in [event.diLepton.leg2()]:
                event.pfmet.setP4(event.pfmet.p4()-(lep.p4()-lep.unscaledP4))
            event.diLepton.met().setP4(event.pfmet.p4())

        if hasattr(event, 'calibratedPuppiMet'):
            event.puppimet = event.calibratedPuppiMet
        else:
            event.puppimet = self.handles['puppiMET'].product()[0]

        if getattr(self.cfg_ana, 'scaleTaus', False):
            self.scaleMet(event, event.diLepton)

        return True

    def testTauVertex(self, tau):
        '''Tests vertex constraints, for tau'''
        # Just checks if the primary vertex the tau was reconstructed with
        # corresponds to the one used in the analysis
        # isPV = tau.vertex().z() == lepton.associatedVertex.z()
        isPV = abs(tau.leadChargedHadrCand().dz()) < 0.2
        return isPV

    def testVertex(self, lepton):
        '''Tests vertex constraints, for mu'''
        return abs(lepton.dxy()) < 0.045 and abs(lepton.dz()) < 0.2

    def testLeg2ID(self, tau):
        # Don't apply anti-e discriminator for relaxed tau ID
        # RIC: 9 March 2015
        return  (tau.tauID('decayModeFinding') > 0.5 and 
                abs(tau.charge()) == 1 and
                # tau.tauID('againstElectronTightMVA5')  > 0.5  and
                # tau.tauID('againstMuonLoose3')         > 0.5  and
                # (tau.zImpact() > 0.5 or tau.zImpact() < -1.5) and
                self.testTauVertex(tau))

    def testLeg2Iso(self, tau, isocut):
        '''if isocut is None, returns true if three-hit iso cut is passed.
        Otherwise, returns true if iso MVA > isocut.'''
        if isocut is None:
            return tau.tauID('byLooseCombinedIsolationDeltaBetaCorr3Hits') > 0.5
        else:
            # JAN FIXME - placeholder, as of now only used to define passing cuts
            # return tau.tauID("byIsolationMVA3newDMwLTraw") > isocut
            # RIC: 9 March 2015
            return tau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits") < isocut

    def testTightElectronID(self, electron):
        '''Selection for electron from tau decay'''
        return electron.mvaIDRun2('Spring16', 'POG80')

    def testElectronID(self, electron):
        '''Loose selection for generic electrons'''
        return electron.mvaIDRun2('Spring16', 'POG90')

    def testVetoElectronID(self, electron):
        #return cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto')
        return electron.cutBasedId('POG_SPRING16_25ns_v1_Veto') # cut based Summer 16 veto ID for di-electron-veto on twiki MSSM # POG Spring15 25ns cut-based "Veto" ID on twiki HTTT

    def testLeg1ID(self, electron):
        '''Tight electron selection, no isolation requirement.
        '''

        cVeto = electron.passConversionVeto()
        mHits = electron.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1

        return self.testTightElectronID(electron) and self.testVertex(electron) and (cVeto and mHits)

    def testLeg1Iso(self, leg, isocut):  # electron
        if isocut is None:
            isocut = self.cfg_ana.iso2
        return leg.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < isocut

    def testLooseleg1(self, leg):  # electrons
        ''' pt, eta and isolation selection for electrons
            used in the di-electron veto.
            pt 15, eta 2.5, dB relIso 0.3
        '''
        return (leg.pt() > 15 and abs(leg.eta()) < 2.5 and self.testVetoElectronID(leg) and self.testVertex(leg) and leg.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.3)

    def testTightOtherLepton(self, muon):
        '''Tight muon selection, no isolation requirement'''
        return muon.muonIDMoriond17() and \
            self.testVertex(muon) and \
            abs(muon.eta()) < 2.4 and \
            muon.pt() > 10. and \
            muon.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0) < 0.3

    def thirdLeptonVeto(self, leptons, otherLeptons, isoCut=0.3):
        # count veto muons
        vOtherLeptons = [muon for muon in otherLeptons if
                         muon.muonID("POG_ID_Medium_Moriond") and # muon.muonIDMoriond17() and
                         self.testVertex(muon) and
                         self.testLegKine(muon, ptcut=10, etacut=2.4) and
                         muon.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0) < 0.3]

        if len(vOtherLeptons) > 0:
            return False

        return True

    def otherLeptonVeto(self, leptons, otherLeptons, isoCut=0.3):
        # count electrons
        vLeptons = [electron for electron in leptons if
                    self.testLegKine(electron, ptcut=10, etacut=2.5) and
                    self.testVertex(electron) and
                    self.testElectronID(electron) and
                    electron.passConversionVeto() and
                    electron.physObj.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and
                    electron.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.3]
        if len(vLeptons) > 1:
            return False

        return True

    def leptonAccept(self, leptons, event):
        '''Returns True if the additional lepton veto is successful'''
        looseLeptons = [l for l in leptons if self.testLooseleg1(l)]
        nLeptons = len(looseLeptons)

        if event.leg1 not in looseLeptons: 
            looseLeptons.append(event.leg1) #TODO why ?
        
        if nLeptons < 2:
            return True
        
        # if there is an opposite-charge electron pair in the event with electrons separated by dR>0.15 and both passing the loose selection
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

    def bestDiLepton(self, diLeptons):
        '''Returns the best diLepton according to Andrew's prescription.'''

        if len(diLeptons) == 1:
            return diLeptons[0]

        least_iso_highest_pt = lambda dl: (dl.leg1().relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0), -dl.leg1().pt(), -dl.leg2().tauID("byIsolationMVArun2v1DBoldDMwLTraw"), -dl.leg2().pt())

        return sorted(diLeptons, key=lambda dil : least_iso_highest_pt(dil))[0]

    def trigMatched(self, event, diL, requireAllMatched=False):

        matched = super(TauEleAnalyzer, self).trigMatched(event, diL, requireAllMatched=requireAllMatched, ptMin=23.)#, relaxIds=[11])

        if matched and len(diL.matchedPaths) == 1 and diL.leg1().pt() <= 33. and 'Ele32' in list(diL.matchedPaths)[0]:
            matched = False

        return matched

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
