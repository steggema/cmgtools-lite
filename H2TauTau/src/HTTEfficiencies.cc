#include "CMGTools/H2TauTau/interface/HTTEfficiencies.h"

#include <vector>

#include "TFile.h"
#include "RooRealVar.h"
#include "RooFunctor.h"

EffProvider::EffProvider() {
  TFile f_in("/afs/cern.ch/user/s/steggema/work/80/CMSSW_8_0_25/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root");
  std::cout << "Creating EffProvider instance in HTTWeighter" << std::endl;
  ws_ = (RooWorkspace*) f_in.Get("w");
  f_in.Close();
}

double getDYWeightWS(double genMass, double genpT) {
    auto ws = EffProvider::instance().ws();
    RooFunctor* zpt_weight = ws.function("zpt_weight")->functor(ws.argSet("z_gen_mass,z_gen_pt"));
    auto args = std::vector<double>{genMass, genpT};
    return zpt_weight->eval(args.data());
}

double getTauIDWeightVLoose(double pt, double eta, double dm) {
  return 0.99;
}

double getTauIDWeightLoose(double pt, double eta, double dm) {
  return 0.99;
}

double getTauIDWeightMedium(double pt, double eta, double dm) {
  return 0.97;
}

double getTauIDWeightTight(double pt, double eta, double dm) {
  return 0.95;
}

double getTauIDWeightVTight(double pt, double eta, double dm) {
  return 0.93;
}

double getTauIDWeight(double pt, double eta, double dm, int WP) { // yeah double dm
    // auto ws = EffProvider::instance().ws();
    // RooFunctor* tau_id_weight = ws.function("t_iso_mva_t_pt40_eta2p1_sf")->functor(ws.argSet("t_pt,t_eta,t_dm"));
    // auto args = std::vector<double>{pt, eta, dm};
    // auto weight = tau_id_weight->eval(args.data());
    // std::cout << "Tau ID weight for pt, eta, dm" << pt << ", " << eta << ", " << dm << " is " << weight << std::endl;
  //return 0.97;    
  if (WP == 1)
    return getTauIDWeightVLoose(pt, eta, dm);
  if (WP == 2)
    return getTauIDWeightLoose(pt, eta, dm);
  if (WP == 3)
    return getTauIDWeightMedium(pt, eta, dm);
  if (WP == 4)
    return getTauIDWeightTight(pt, eta, dm);
  if (WP == 5)
    return getTauIDWeightVTight(pt, eta, dm);
  return 1.; // default = medium ?
}

double getMuToTauWeightLoose(double pt, double eta, double dm) {
    auto aeta = std::abs(eta);
    if (aeta < 0.4)
        return 1.22;
    if (aeta < 0.8)
        return 1.12;
    if (aeta < 1.2)
        return 1.26;
    if (aeta < 1.7)
        return 1.22;
    if (aeta < 2.3)
        return 2.39;
    return 1.;
}

double getMuToTauWeightTight(double pt, double eta, double dm) {
    auto aeta = std::abs(eta);
    if (aeta < 0.4)
        return 1.47;
    if (aeta < 0.8)
        return 1.55;
    if (aeta < 1.2)
        return 1.33;
    if (aeta < 1.7)
        return 1.72;
    if (aeta < 2.3)
        return 2.50;
    return 1.;
}

double getMuToTauWeight(double pt, double eta, double dm, int WP) {
  if (WP == 2)
    return getMuToTauWeightLoose(pt, eta, dm);
  if (WP == 4)
    return getMuToTauWeightTight(pt, eta, dm);
  return 1.; // default = 1 ?
}

double getEToTauWeightVLoose(double pt, double eta, double dm) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.21;
    if (aeta > 1.5)
        return 1.38;
    return 1.;
}

double getEToTauWeightLoose(double pt, double eta, double dm) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.32;
    if (aeta > 1.5)
        return 1.38;
    return 1.;
}

double getEToTauWeightMedium(double pt, double eta, double dm) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.32;
    if (aeta > 1.5)
        return 1.53;
    return 1.;
}

double getEToTauWeightTight(double pt, double eta, double dm) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.40;
    if (aeta > 1.5)
        return 1.90;
    return 1.;
}

double getEToTauWeightVTight(double pt, double eta, double dm) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.21;
    if (aeta > 1.5)
        return 1.97;
    return 1.;
}

double getEToTauWeight(double pt, double eta, double dm, int WP) {
  if (WP == 1)
    return getEToTauWeightVLoose(pt, eta, dm);
  if (WP == 2)
    return getEToTauWeightLoose(pt, eta, dm);
  if (WP == 3)
    return getEToTauWeightMedium(pt, eta, dm);
  if (WP == 4)
    return getEToTauWeightTight(pt, eta, dm);
  if (WP == 5)
    return getEToTauWeightVTight(pt, eta, dm);
  return 1.; // default = 1 ?
}

double getTauWeight(int gen_match, double pt, double eta, double dm, int ele_WP, int mu_WP, int tau_WP) {
  // 1 = VLoose .... 5 = VTight
    if (gen_match == 5)
        return getTauIDWeight(pt, eta, dm, tau_WP);
    if (gen_match == 2 || gen_match == 4)
        return getMuToTauWeight(pt, eta, dm, mu_WP);
    if (gen_match == 1 || gen_match == 3)
        return getEToTauWeight(pt, eta, dm, ele_WP);
    return 1.;
}
