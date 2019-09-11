from array import array
import ROOT

ROOT.gStyle.SetPaintTextFormat('1.2f')
ROOT.gStyle.SetOptStat(0)

do1D = False
do2D = True

cut_gentau = 'tau_gen_match==5 && gen_dm==1'
# cut_gentau = 'tau_gen_match==5'
# cut_gentau = 'tau_gen_match==6'

cut_no_pu = cut_gentau + '&& n_true_interactions < 1'
# cut_hi_pu = cut_gentau + '&& n_true_interactions > 50'
cut_hi_pu = cut_gentau + '&& n_true_interactions > 65'
# cut_hi_pu = cut_gentau + '&& n_true_interactions<30 && n_true_interactions>20'

outdir = 'plots_dm1_pu65/'
# outdir = 'plots/'
# outdir = 'plots_jets/'

if __name__ == '__main__':
    f_in = ROOT.TFile('IsoStudyMorePhotons/DYJetsToLL_M50_LO/TauIsoTreeProducer/tree.root')
    tree = f_in.Get('tree')

    cv = ROOT.TCanvas('canvas', '', 700, 600)
    n_no_pu = tree.Draw('1', cut_no_pu)
    n_hi_pu = tree.Draw('1', cut_hi_pu)
    for lch in ['_lch[0]', '_lph', '_lch', '']:
        # 1D
        if do1D:
            for (pt_min, pt_max) in [(1, 1.5), (1.5, 2), (2, 3), (3, 4), (4, 5), (5, 10), (10, 20), (20, 1000)]:
                # for (eta_min, eta_max) in [(0., 0.025), (0.025, 0.05), (0.05, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.5)]:
                for draw_var in ["abs(tau_ph_dphi{})".format(lch), "abs(tau_ph_deta{})".format(lch)]:
                    phi_no_pu = ROOT.TH1F('phi_no_pu', '', 50, 0., 0.5)
                    phi_hi_pu = ROOT.TH1F('phi_hi_pu', '', 50, 0., 0.5)

                    lead = '[0]' if '[0]' in lch else ''

                    ph_pt_cut = 'tau_ph_pt{}>{} && tau_ph_pt{}<{}'.format(lead, pt_min, lead, pt_max)
                    if lch == '_lph':
                        ph_pt_cut += '&& tau_ph_deta_lph >0.' # Remove leading photons
                    # ph_pt_cut += '&& tau_ph_deta{}>={} && tau_ph_deta{}<={}'.format(lch, eta_min, lch, eta_max)
                    # draw_var = "abs(tau_ph_dphi{})".format(lch)

                    tree.Project(phi_no_pu.GetName(), draw_var, "({} && {})/{}.".format(ph_pt_cut, cut_no_pu, n_no_pu))
                    tree.Project(phi_hi_pu.GetName(), draw_var, "({} && {})/{}.".format(ph_pt_cut, cut_hi_pu, n_hi_pu))

                    phi_no_pu.GetXaxis().SetTitle('|#Delta#phi|' if 'phi' in draw_var else '|#Delta#eta|')
                    phi_no_pu.GetYaxis().SetTitle('Frequency')

                    phi_no_pu.Draw()
                    # cv.Print(outdir+'phi_pt{}_eta{}.png'.format(pt_min, str(eta_min).replace('.', 'p')))
                    cv.Print(outdir+'{}_pt{}{}.png'.format('phi' if 'phi' in draw_var else 'eta', pt_min, lch.replace('[0]', 'lead')))

                    phi_no_pu_cum = phi_no_pu.GetCumulative()
                    phi_no_pu_cum.Scale(1./phi_no_pu.Integral())
                    phi_no_pu_cum.GetYaxis().SetTitle('Cumulative')
                    phi_no_pu_cum.Draw()
                    cv.Print(outdir+'{}_cum_pt{}{}.png'.format('phi' if 'phi' in draw_var else 'eta', pt_min, lch.replace('[0]', 'lead')))

                    phi_no_pu.Divide(phi_hi_pu)
                    phi_no_pu.GetYaxis().SetTitle('P(coming from tau)')
                    phi_no_pu.Draw()

                    # cv.Print(outdir+'p_phi_pt{}_eta{}{}.png'.format(pt_min, str(eta_min).replace('.', 'p'), lch))
                    cv.Print(outdir+'p_{}_pt{}{}.png'.format('phi' if 'phi' in draw_var else 'eta', pt_min, lch.replace('[0]', 'lead')))

        if do2D:
            bins_eta = array('f', [0.0, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.5])
            bins_phi = array('f', [0.0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.2, 0.3, 0.5])

            for (pt_min, pt_max) in [(1, 1.5), (1.5, 2), (2, 3), (3, 4), (4, 5), (5, 10), (10, 1000)]:
                no_pu = ROOT.TH2F('no_pu', '', len(bins_eta) - 1, bins_eta, len(bins_phi) - 1, bins_phi)
                hi_pu = ROOT.TH2F('hi_pu', '', len(bins_eta) - 1, bins_eta, len(bins_phi) - 1, bins_phi)

                # Ensure only variables pertaining to the leading photon are taken such that only the leading photon is drawn
                lead = '[0]' if '[0]' in lch else ''

                ph_pt_cut = 'tau_ph_pt{}>{} && tau_ph_pt{}<{}'.format(lead, pt_min, lead, pt_max)
                if lch == '_lph':
                    ph_pt_cut += '&& tau_ph_deta_lph >0.' # Remove leading photons

                draw_var = "abs(tau_ph_dphi{}):abs(tau_ph_deta{})".format(lch, lch)

                tree.Project(no_pu.GetName(), draw_var, "tau_ph_pt{}*({} && {})/{}.".format(lead, ph_pt_cut, cut_no_pu, n_no_pu))
                tree.Project(hi_pu.GetName(), draw_var, "tau_ph_pt{}*({} && {})/{}.".format(lead, ph_pt_cut, cut_hi_pu, n_hi_pu))
                
                no_pu.GetYaxis().SetTitle('|#Delta#phi|')
                no_pu.GetXaxis().SetTitle('|#Delta#eta|')

                no_pu_int_eta = no_pu.Clone('no_pu_int_eta')
                no_pu_int_phi = no_pu.Clone('no_pu_int_phi')
                no_pu_int_etaphi = no_pu.Clone('no_pu_int_etaphi')

                nbinsx = no_pu_int_eta.GetNbinsX()
                nbinsy = no_pu_int_eta.GetNbinsY()

                for i_eta in xrange(nbinsx):
                    for i_phi in xrange(nbinsy):
                        c_eta = no_pu.Integral(i_eta + 1, i_eta + 1, 1, i_phi + 1)/no_pu.Integral(i_eta + 1, i_eta + 1, 1, nbinsy) if no_pu.Integral(i_eta + 1, i_eta + 1, 1, nbinsy) else 0.
                        c_phi = no_pu.Integral(1, i_eta + 1, i_phi + 1, i_phi + 1)/no_pu.Integral(1, nbinsx, i_phi + 1, i_phi + 1) if no_pu.Integral(1, nbinsx, i_phi + 1, i_phi + 1) else 0.
                        c_etaphi =  0.
                        if no_pu.Integral() == 0.:
                            print draw_var, "tau_ph_pt{}*({} && {})/{}.".format(lead, ph_pt_cut, cut_no_pu, n_no_pu)
                        else:
                            c_etaphi = no_pu.Integral(1, i_eta + 1, 1, i_phi + 1)/no_pu.Integral()
                        no_pu_int_eta.SetBinContent(i_eta + 1, i_phi + 1, c_eta)
                        no_pu_int_phi.SetBinContent(i_eta + 1, i_phi + 1, c_phi)
                        no_pu_int_etaphi.SetBinContent(i_eta + 1, i_phi + 1, c_etaphi)

                no_pu_int_eta.Draw('colz text')
                cv.Print(outdir+'intphi_phivseta_pt{}{}.png'.format(pt_min, lch.replace('[0]', 'lead')))

                no_pu_int_phi.Draw('colz text')
                cv.Print(outdir+'inteta_phivseta_pt{}{}.png'.format(pt_min, lch.replace('[0]', 'lead')))

                no_pu_int_etaphi.Draw('colz text')
                cv.Print(outdir+'intetaphi_phivseta_pt{}{}.png'.format(pt_min, lch.replace('[0]', 'lead')))

                # Divide by bin size
                no_pu.Scale(1., 'width')
                hi_pu.Scale(1., 'width')


                no_pu.Draw('colz text')
                cv.Print(outdir+'f_phivseta_pt{}{}.png'.format(pt_min, lch.replace('[0]', 'lead')))

                no_pu.Divide(hi_pu)
                no_pu.Draw('colz text')
                no_pu.GetZaxis().SetRangeUser(0., 1.)
                cv.Print(outdir+'p_phivseta_pt{}{}.png'.format(str(pt_min).replace('.', 'p'), lch.replace('[0]', 'lead')))
