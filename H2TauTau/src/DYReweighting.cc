#include "CMGTools/H2TauTau/interface/DYReweighting.h"

#include <TROOT.h>
#include <TTree.h>
#include <iostream>

HistProvider::HistProvider() {
  f_in = new TFile("/afs/cern.ch/work/d/dwinterb/public/MSSM2016/zpt_weights_summer2016_v2.root");
  std::cout << "Creating HistProvider instance in DYReweighting" << std::endl;
  h_zptmass = dynamic_cast<TH2D*>(f_in->Get("zptmass_histo"));
  if (!h_zptmass)
    std::cerr << "ERROR: Not getting histogram out of file in DYReweighting" << std::endl;
}

HistProvider::~HistProvider() {
  delete f_in;
}

double getDYWeight(double genMass, double genpT) {
    const TH2D& h_zptmass = HistProvider::instance().hist();
    double weight = h_zptmass.GetBinContent(h_zptmass.GetXaxis()->FindBin(genMass), h_zptmass.GetYaxis()->FindBin(genpT));
    if (weight == 0.) {
        std::cout << "WARNING: Zero weight in DY reweighting: " << std::endl;
        std::cout << "   DY weight " << weight << std::endl;
        std::cout << "   genMass " << genMass << std::endl;
        std::cout << "   genpT " << genpT << std::endl;
    }
    return weight;
}

