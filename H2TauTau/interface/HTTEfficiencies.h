#ifndef __CMGTools_H2TauTau_HTTEfficiencies__
#define __CMGTools_H2TauTau_HTTEfficiencies__

#include "RooWorkspace.h"

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
    EffProvider();
    ~EffProvider() {}
    RooWorkspace* ws_;
};


double getDYWeightWS(double genMass, double genpT);

double getTauIDWeightVLoose(double pt, double eta, double dm);

double getTauIDWeightLoose(double pt, double eta, double dm);

double getTauIDWeightMedium(double pt, double eta, double dm);

double getTauIDWeightTight(double pt, double eta, double dm);

double getTauIDWeightVTight(double pt, double eta, double dm);

double getTauIDWeight(double pt, double eta, double dm, int WP);

double getMuToTauWeightLoose(double pt, double eta, double dm);

double getMuToTauWeightTight(double pt, double eta, double dm);

double getMuToTauWeight(double pt, double eta, double dm, int WP);

double getEToTauWeightVLoose(double pt, double eta, double dm);

double getEToTauWeightLoose(double pt, double eta, double dm);

double getEToTauWeightMedium(double pt, double eta, double dm);

double getEToTauWeightTight(double pt, double eta, double dm);

double getEToTauWeightVTight(double pt, double eta, double dm);

double getEToTauWeight(double pt, double eta, double dm, int WP);

double getTauWeight(int gen_match, double pt, double eta, double dm, int ele_WP, int mu_WP, int tau_WP);

#endif
