#ifndef __CMGTools_H2TauTau_DYReweighting__
#define __CMGTools_H2TauTau_DYReweighting__

#include <TFile.h>
#include <TH2D.h>

double getDYWeight(double genMass, double genpT);

class HistProvider {
public:
    static HistProvider& instance() {
        static HistProvider instance;
        return instance;
    }

    const TH2D& hist() const {
        return *h_zptmass;
    }

private:
    HistProvider();
    ~HistProvider();

    TFile* f_in;
    TH2D* h_zptmass;
};

#endif
