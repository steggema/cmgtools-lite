from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi

def n_photons_tau(tau):
    n_ph = 0
    for ph in tau.signalGammaCands():
        if ph.pt() > 0.5:
            n_ph += 1
    for ph in tau.isolationGammaCands():
        if ph.pt() > 0.5:
            n_ph += 1
    return n_ph

def e_over_h(tau):
    total = tau.ecalEnergy() + tau.hcalEnergy()
    return tau.ecalEnergy()/total if total > 0. else -1.

def pt_weighted_dx(tau, mode=0, var=0, decaymode=-1):
    sum_pt = 0.;
    sum_dx_pt = 0.;
    signalrad = max(0.05, min(0.1, 3./max(1., tau.pt())))
    cands = getGammas(tau, mode < 2)
    for cand in cands:
        if cand.pt() < 0.5:
          continue;
        dr = deltaR(cand, tau)
        deta = abs(cand.eta() - tau.eta())
        dphi = abs(deltaPhi(cand.phi(), tau.phi()))
        pt = cand.pt()
        flag = isInside(pt, deta, dphi)
        if decaymode != 10:
            if mode == 2 or (mode == 0 and dr < signalrad) or (mode == 1 and dr > signalrad):
                sum_pt += pt
                if var == 0:
                  sum_dx_pt += pt * dr
                elif var == 1:
                  sum_dx_pt += pt * deta
                elif var == 2:
                  sum_dx_pt += pt * dphi
        else:
            if (mode == 2 and flag == False) or (mode == 1 and flag == True) or mode==0:
                sum_pt += pt
                if var == 0:
                  sum_dx_pt += pt * dr
                elif var == 1:
                  sum_dx_pt += pt * deta
                elif var == 2:
                  sum_dx_pt += pt * dphi
    if sum_pt > 0.:
        return sum_dx_pt/sum_pt;
    return 0.

def tau_pt_weighted_dr_iso(tau):
    return pt_weighted_dx(tau, 2, 0, tau.decayMode())

def tau_pt_weighted_dphi_strip(tau):
    dm = tau.decayMode()
    return pt_weighted_dx(tau, 2 if dm == 10 else 1, 2, dm)

def tau_pt_weighted_deta_strip(tau):
    dm = tau.decayMode()
    return pt_weighted_dx(tau, 2 if dm == 10 else 1, 1, dm)

def tau_pt_weighted_dr_signal(tau):
    return pt_weighted_dx(tau, 0, 0, tau.decayMode())

def getGammas(tau, signal=True):
    if signal:
        return tau.signalGammaCands()
    return tau.isolationGammaCands()


def isInside(photon_pt, deta, dphi):
    stripEtaAssociationDistance_0p95_p0 = 0.197077
    stripEtaAssociationDistance_0p95_p1 = 0.658701
    stripPhiAssociationDistance_0p95_p0 = 0.352476
    stripPhiAssociationDistance_0p95_p1 = 0.707716
    if photon_pt == 0.:
        return False
    if dphi < 0.3 and dphi < max(0.05, stripPhiAssociationDistance_0p95_p0*pow(photon_pt, -stripPhiAssociationDistance_0p95_p1)) and  deta<0.15 and deta<max(0.05, stripEtaAssociationDistance_0p95_p0*pow(photon_pt, -stripEtaAssociationDistance_0p95_p1)):
        return True
    return False
