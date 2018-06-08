#include <vector>

#include "TFile.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "RooFunctor.h"

class EffProvider {
public:
    static EffProvider& instance() {
        static EffProvider instance;
        return instance;
    }

    const RooWorkspace& ws() const {
        return *ws_;
    }

private:
    EffProvider() {
        TFile f_in("/afs/cern.ch/user/s/steggema/work/80/CMSSW_8_0_25/src/CMGTools/H2TauTau/data/htt_scalefactors_v16_5.root");
        std::cout << "Creating EffProvider instance in HTTWeighter" << std::endl;
        ws_ = (RooWorkspace*) f_in.Get("w");
        f_in.Close();
    }

    ~EffProvider() {
    }
    RooWorkspace* ws_;
};


double getDYWeightWS(double genMass, double genpT) {
    auto ws = EffProvider::instance().ws();
    RooFunctor* zpt_weight = ws.function("zpt_weight")->functor(ws.argSet("z_gen_mass,z_gen_pt"));
    auto args = std::vector<double>{genMass, genpT};
    return zpt_weight->eval(args.data());
}

double getTauIDWeight(double pt, double eta, double dm) { // yeah double dm
    // auto ws = EffProvider::instance().ws();
    // RooFunctor* tau_id_weight = ws.function("t_iso_mva_t_pt40_eta2p1_sf")->functor(ws.argSet("t_pt,t_eta,t_dm"));
    // auto args = std::vector<double>{pt, eta, dm};
    // auto weight = tau_id_weight->eval(args.data());
    // std::cout << "Tau ID weight for pt, eta, dm" << pt << ", " << eta << ", " << dm << " is " << weight << std::endl;
  return 0.97;
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

double getMuToTauWeightLoose(double eta) {
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

double getMuToTauWeightTight(double eta) {
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

double getEToTauWeightVLoose(double eta) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.21;
    if (aeta > 1.5)
        return 1.38;
    return 1.;
}

double getEToTauWeightLoose(double eta) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.32;
    if (aeta > 1.5)
        return 1.38;
    return 1.;
}

double getEToTauWeightMedium(double eta) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.32;
    if (aeta > 1.5)
        return 1.53;
    return 1.;
}

double getEToTauWeightTight(double eta) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.40;
    if (aeta > 1.5)
        return 1.90;
    return 1.;
}

double getEToTauWeightVTight(double eta) {
    auto aeta = std::abs(eta);
    if (aeta < 1.5)
        return 1.21;
    if (aeta > 1.5)
        return 1.97;
    return 1.;
}

double getTauWeight(int gen_match, double pt, double eta, double dm) {
    if (gen_match == 5)
        return getTauIDWeight(pt, eta, dm);
    if (gen_match == 2 || gen_match == 4)
        return getMuToTauWeightLoose(eta);
    if (gen_match == 1 || gen_match == 3)
        return getEToTauWeightVLoose(eta);
    return 1.;
}
