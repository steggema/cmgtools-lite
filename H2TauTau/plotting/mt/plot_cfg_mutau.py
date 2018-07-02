import copy
from collections import namedtuple
from operator import itemgetter

from numpy import array

from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg, VariableCfg
from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistograms, createTrees
from CMGTools.H2TauTau.proto.plotter.HistDrawer import HistDrawer
from CMGTools.H2TauTau.proto.plotter.Variables import taumu_vars, getVars
from CMGTools.H2TauTau.proto.plotter.helper_methods import getVertexWeight
from CMGTools.H2TauTau.proto.samples.fall17.htt_common import lumi

from CMGTools.H2TauTau.proto.plotter.qcdEstimationMSSMltau import estimateQCDWMSSM, createQCDWHistograms
from CMGTools.H2TauTau.proto.plotter.defaultGroups import createDefaultGroups

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.metrics import ams_hists

Cut = namedtuple('Cut', ['name', 'cut'])

binning_mssm = array([0.,10.,20.,30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,225.,250.,275.,300.,325.,350.,400.,500.,700.,900.,1100.,1300.,1500.,1700.,1900.,2100.,2300.,2500.,2700.,2900.,3100.,3300.,3500.,3700.,3900.])

binning_mssm_btag = array([0.,20.,40.,60.,80.,100.,120.,140.,160.,180.,200.,250.,300.,350.,400.,500.,700.,900.,1100.,1300.,1500.,1700.,1900.,2100.,2300.,2500.,2700.,2900.,3100.,3300.,3500.,3700.,3900.])

binning_mva = array([0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.925, 0.95, 0.975, 0.985, 0.9925, 1.001])
binning_mva2 = array([0., 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.925, 0.95, 0.975, 1.001])

def prepareCuts(mode):
    cuts = []
    inc_cut = '&&'.join([cat_Inc])
    # inc_cut += '&& l2_decayModeFinding'

    mt_cut = 'mt<30'
    if mode in ['sm', 'iso', 'cp', 'mva', 'pog']:
        mt_cut = 'mt<40'
        # inc_cut += '&& n_bjets==0'

    
    # cuts.append(Cut('inclusive_tauisosideband', inc_cut.replace('l2_byIsolationMVArun2v1DBoldDMwLT>3.5', 'l2_byIsolationMVArun2v1DBoldDMwLT<3.5&&l2_byIsolationMVArun2v1DBoldDMwLT>0.5') + '&& l1_charge != l2_charge'))

    # cuts.append(Cut('inclusive', inc_cut + '&& l1_charge != l2_charge'))
    # cuts.append(Cut('inclusivemt40', inc_cut + '&& l1_charge != l2_charge && mt<40'))

    # MSSM Categories

    if 'mssm' in mode:
        cuts.append(Cut('nobtag', inc_cut + '&& l1_charge != l2_charge && n_bjets==0 && mt<30'))
        cuts.append(Cut('btag', inc_cut + '&& l1_charge != l2_charge && n_bjets>=1 && n_jets<=1 && mt<30'))
    if mode == 'mssm_signal':
        cuts.append(Cut('nobtag_highmtos', inc_cut + '&& l1_charge != l2_charge && n_bjets==0 && mt>70'))
        cuts.append(Cut('nobtag_highmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets==0 && mt>70'))
        cuts.append(Cut('nobtag_lowmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets==0 && mt<30'))

    if mode == 'mssm_signal':
        cuts.append(Cut('btag_highmtos', inc_cut + '&& l1_charge != l2_charge && n_bjets>=1 && n_jets<=1 && mt>70'))
        cuts.append(Cut('btag_highmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets>=1 && n_jets<=1 && mt>70'))
        cuts.append(Cut('btag_lowmtss', inc_cut + '&& l1_charge == l2_charge && n_bjets>=1 && n_jets<=1 && mt<30'))

    if mode in ['sm', 'pog']:
        cuts.append(Cut('inclusive', inc_cut + '&&  l1_charge != l2_charge'))
        cuts.append(Cut('lowmt', inc_cut + '&& l1_charge != l2_charge && mt<30'))
        cuts.append(Cut('lowmt_dm0', inc_cut + '&& l1_charge != l2_charge && mt<30 && l2_decayMode==0'))
        cuts.append(Cut('lowmt_dm1', inc_cut + '&& l1_charge != l2_charge && mt<30 && l2_decayMode==1'))
        cuts.append(Cut('lowmt_dm10', inc_cut + '&& l1_charge != l2_charge && mt<30 && l2_decayMode==10'))
        cuts.append(Cut('lowmt_lowmvis_pzetadisc_lowmuonpt', inc_cut + '&& l1_charge != l2_charge && mt<30 && mvis<100 && pzeta_disc>-40. && l1_pt<45.'))
        # cuts.append(Cut('inclusive_dm0', inc_cut + '&&  l1_charge != l2_charge && l2_decayMode==0'))
        # cuts.append(Cut('inclusive_dm1', inc_cut + '&&  l1_charge != l2_charge && l2_decayMode==1'))
        # cuts.append(Cut('inclusive_dm10', inc_cut + '&&  l1_charge != l2_charge && l2_decayMode==10'))
        # mssm_pt_cuts = '&& l2_pt>30'
        # cuts.append(Cut('inclusive_mssmcuts', inc_cut + mssm_pt_cuts + '&&  l1_charge != l2_charge'))
        # cuts.append(Cut('inclusive_mssmcuts_dm0', inc_cut + mssm_pt_cuts + '&&  l1_charge != l2_charge && l2_decayMode==0'))
        # cuts.append(Cut('inclusive_mssmcuts_dm1', inc_cut + mssm_pt_cuts + '&&  l1_charge != l2_charge && l2_decayMode==1'))
        # cuts.append(Cut('inclusive_mssmcuts_dm10', inc_cut + mssm_pt_cuts + '&&  l1_charge != l2_charge && l2_decayMode==10'))

        # cuts.append(Cut('inclusive_btag', inc_cut.replace('n_bjets==0', 'n_bjets>0') + '&&  l1_charge != l2_charge'))
        # cuts.append(Cut('inclusive_btag_pfmtgr70', inc_cut.replace('n_bjets==0', 'n_bjets>0') + '&&  l1_charge != l2_charge && pfmet_mt1>70'))
        # cuts.append(Cut('inclusive_pfmtgr70', inc_cut + '&&  l1_charge != l2_charge && pfmet_mt1>70'))
        # cuts.append(Cut('inclusive_pfmt40', inc_cut + '&&  l1_charge != l2_charge && pfmet_mt1<40'))
        # cuts.append(Cut('0jet_pfmt40', inc_cut + '&& l1_charge != l2_charge && pfmet_mt1<40 && n_jets<0.5'))
        # cuts.append(Cut('gr1jet_pfmt40', inc_cut + '&& l1_charge != l2_charge && pfmet_mt1<40 && n_jets>0.5'))


        do_run1_cats = False
        if do_run1_cats:
            cuts.append(Cut('0jet_medium', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets<0.5 && l2_pt>30. && l2_pt<45.'))
            cuts.append(Cut('0jet_high', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets<0.5 && l2_pt>45.'))

            cut_vbf = '(vbf_mjj>500. && abs(vbf_deta)>3.5 && vbf_n_central==0.)'
            cut_vbf_tight = '(vbf_mjj>700. && abs(vbf_deta)>4.0 && vbf_n_central==0. && pthiggs>100.)'
            cut_vbf_loose = '({cut_vbf} && !({cut_vbf_tight}))'.format(cut_vbf=cut_vbf, cut_vbf_tight=cut_vbf_tight)

            cuts.append(Cut('1jet_medium', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets>0.5 && l2_pt>30. && l2_pt<45. && !{vbf}'.format(vbf=cut_vbf)))
            cuts.append(Cut('1jet_high_lowhiggspt', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets>0.5 && l2_pt>45. && pthiggs<100. && !{vbf}'.format(vbf=cut_vbf)))
            cuts.append(Cut('1jet_high_highhiggspt', inc_cut + '&& l1_charge != l2_charge && mt<40 && n_jets>0.5 && l2_pt>45. && pthiggs>100. && !{vbf}'.format(vbf=cut_vbf)))
            cuts.append(Cut('vbf', inc_cut + '&& l1_charge != l2_charge && mt<40 && {vbf}'.format(vbf=cut_vbf)))

            cuts.append(Cut('vbf_loose', inc_cut + '&& l1_charge != l2_charge && l2_pt>30. && mt<40 && {vbf}'.format(vbf=cut_vbf_loose)))
            cuts.append(Cut('vbf_tight', inc_cut + '&& l1_charge != l2_charge && l2_pt>30. && mt<40 && {vbf}'.format(vbf=cut_vbf_tight)))

    if mode == 'cp':
        cuts.append(Cut('inclusivemt40', inc_cut + '&&  l1_charge != l2_charge && mt<40 && mvis>40 && mvis<90 && l2_nc_ratio>-99'))

    if mode == 'iso':
        cuts = []
        cuts.append(Cut('inclusivemtgr60', inc_cut + '&& l1_charge != l2_charge && mt>70 && n_jets<0.5'))
        # cuts.append(Cut('inclusivemtgr40antiiso', inc_cut.replace('l1_reliso05<0.1', 'l1_reliso05>0.2') + '&& l1_charge != l2_charge && mt>40'))
        cuts.append(Cut('inclusivemtgr60antiiso', inc_cut.replace('l2_byIsolationMVArun2v1DBoldDMwLT>3.5', 'l2_byIsolationMVArun2v1DBoldDMwLT<3.5') + '&& l1_charge != l2_charge && mt>70 && n_jets<0.5'))

    # cuts.append(Cut('SS', inc_cut + '&& l1_charge == l2_charge'))
    # cuts.append(Cut('SS_muantiiso', inc_cut.replace('l1_reliso05<0.1', 'l1_reliso05>0.2') + '&& l1_charge == l2_charge'))
    # cuts.append(Cut('SSmt40', inc_cut + '&& l1_charge == l2_charge && mt<40'))
    # cuts.append(Cut('SShighmt40', inc_cut + '&& l1_charge == l2_charge && mt>40'))

    return cuts, mt_cut

def createSamples(mode, analysis_dir, total_weight, qcd_from_same_sign, w_qcd_mssm_method, r_qcd_os_ss):
    hist_dict = {}
    sample_dict = {}

    samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir, mode=mode)

    if mode == 'mssm_control' or not 'mssm' in mode:
        all_samples = [s for s in all_samples if not 'ggH' in s.name and not 'bbH' in s.name]

    sample_dict['all_samples'] = all_samples

    if qcd_from_same_sign and not w_qcd_mssm_method:
        samples_qcdfromss = [s for s in all_samples if s.name != 'QCD']
        samples_ss = copy.deepcopy(samples_qcdfromss)

        samples_ss = [s for s in samples_ss if not s.is_signal]

        for sample in samples_ss:
            if sample.name != 'data_obs':
                # Subtract background from data
                sample.scale = -1.

        qcd = HistogramCfg(name='QCD', var=None, cfgs=samples_ss, cut=None, total_scale=r_qcd_os_ss, lumi=int_lumi, weight=total_weight)

        samples_qcdfromss.append(qcd)
        sample_dict['samples_qcdfromss'] = samples_qcdfromss

    if w_qcd_mssm_method:
        sample_dict['samples_mssm_method'] = createQCDWHistograms(samples, hist_dict, int_lumi, weight=total_weight, r_qcd_os_ss=r_qcd_os_ss)

    return sample_dict, hist_dict

def createVariables(mode):
    # Taken from Variables.py; can get subset with e.g. getVars(['mt', 'mvis'])
    # variables = taumu_vars
    # variables = getVars(['_norm_', 'mt', 'mvis', 'l1_pt', 'l2_pt', 'l1_eta', 'l2_eta', 'n_vertices', 'n_jets', 'n_bjets'])

    variables = []
    if mode in ['sm', 'pog']:
        # MVA training variables, and others
        variables += getVars(['mt', 'l2_mt', 'n_jets', 'met_pt', 'pthiggs', 'l2_pt', 'l1_pt','mvis', 'l1_eta', 'l2_eta', 'pzeta_disc', 'jet1_pt', 'jet1_eta', 'n_vertices', 'rho', 'dil_pt', 'l2_byIsolationMVArun2v1DBoldDMwLTraw', 'l2_byCombinedIsolationDeltaBetaCorrRaw3Hits', 'l2_byIsolationMVArun2v1DBoldDMwLTraw_zoom',
            'l2_nc_ratio', 'l2_pt_weighted_dr_iso', 'l2_pt_weighted_dr_signal', 'l2_pt_weighted_dphi_strip', 'l2_pt_weighted_deta_strip', 'l2_flightLength', 'l2_flightLengthSig', 'l2_dxy_Sig', 'l2_ip3d', 'l2_ip3d_Sig', 'l2_e_over_h', 'l2_n_photons', ])#  'svfit_transverse_mass',  'delta_phi_l1_l2', 'delta_eta_l1_l2', 'pt_l1l2', 'delta_phi_j1_met',

        # variables = taumu_vars

    if mode == 'cp':
        variables = getVars(['l2_nc_ratio'])

    if mode == 'mssm_signal':
        variables = [
            VariableCfg(name='svfit_transverse_mass', binning=binning_mssm, unit='GeV', xtitle='m_{T,SVFit}'),
            VariableCfg(name='svfit_mass', binning=binning_mssm, unit='GeV', xtitle='m_{SVFit}'),
            VariableCfg(name='mvis', binning=binning_mssm, unit='GeV', xtitle='m_{vis}'),
        ]

    if mode == 'iso':
        variables = getVars(['mt', 'l1_pt', 'l2_pt', 'l1_eta', 'l2_eta'])

    return variables

def makePlots(variables, cuts, total_weight, sample_dict, hist_dict, qcd_from_same_sign, w_qcd_mssm_method, mt_cut, friend_func, dc_postfix, make_plots=True, create_trees=False):
    ams_dict = {}
    sample_names = set()
    for cut in cuts:
        if qcd_from_same_sign and not 'SS' in cut.name and not w_qcd_mssm_method:
            cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=sample_dict['samples_qcdfromss'], cut=cut.cut, lumi=int_lumi, weight=total_weight)
        elif w_qcd_mssm_method:
            cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=sample_dict['samples_mssm_method'], cut=cut.cut, lumi=int_lumi, weight=total_weight)
            hist_dict['wjets'].cut = cut.cut # since wjets is a sub-HistogramCfg
        else:
            cfg_main = HistogramCfg(name=cut.name, var=None, cfgs=sample_dict['all_samples'], cut=cut.cut, lumi=int_lumi, weight=total_weight)
        
        if qcd_from_same_sign and not 'SS' in cut.name:
            hist_dict['qcd'].cut = cut.cut.replace('l1_charge != l2_charge', 'l1_charge == l2_charge')

        if w_qcd_mssm_method:
            estimateQCDWMSSM(hist_dict, cut, mt_cut, friend_func=friend_func, r_qcd_os_ss=r_qcd_os_ss)

        cfg_main.vars = variables
        if qcd_from_same_sign:
            hist_dict['qcd'].vars = variables # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
        if w_qcd_mssm_method:
            hist_dict['wjets'].vars = variables # Can put into function but we will not want it by default if we take normalisations from e.g. high MT
            hist_dict['qcd'].vars = variables
            hist_dict['wjets_ss'].vars = variables

        for variable in variables:
            if variable.name in ['svfit_mass', 'svfit_transverse_mass', 'mvis'] and 'mssm' in mode:
                if cut.name in ['inclusive', 'nobtag']:
                    variable.binning = binning_mssm
                elif cut.name in ['btag']:
                    variable.binning = binning_mssm_btag

        if create_trees:
            createTrees(cfg_main, '/data1/steggema/mt/MVATrees', verbose=True)
            continue

        plots = createHistograms(cfg_main, verbose=False, friend_func=friend_func)
        for variable in variables:
        # for plot in plots.itervalues():
            plot = plots[variable.name]
            createDefaultGroups(plot)
            if not w_qcd_mssm_method:
                plot.Group('W', ['W', 'W1Jets', 'W2Jets', 'W3Jets', 'W4Jets'])
            plot.Group('Electroweak', ['VV', 'W'])
            # plot.Group('Single t', ['T_tWch', 'TBar_tWch', 'TToLeptons_sch', 'TToLeptons_tch'])
            plot.Group('ZTT', ['ZTT', 'ZJ'], style=plot.Hist('ZTT').style)
            if make_plots:
                HistDrawer.draw(plot, plot_dir='plots/'+cut.name)
            if variable.name in ['mvis', 'svfit_transverse_mass', 'svfit_mass', 'mva', 'mva2div1', 'mva1', 'mva2', 'l2_nc_ratio']:
                plot.WriteDataCard(filename='datacard_{mode}_{var}.root'.format(mode=mode, var=variable.name), dir='mt_' + cut.name, mode='UPDATE', postfix=dc_postfix) #mt = mu-tau
            for signal_hist in plot.SignalHists():
                sample_names.add(signal_hist.name)
                ams_dict[variable.name + '__' + cut.name + '__' + signal_hist.name + '_'] = ams_hists(signal_hist.weighted, plot.BGHist().weighted)

    print '\nOptimisation results:'
    all_vals = ams_dict.items()
    for sample_name in sample_names:
        vals = [v for v in all_vals if sample_name + '_' in v[0]]
        vals.sort(key=itemgetter(1))
        for key, item in vals:
            print item, key

        print '\nBy variable'
        for variable in variables:
            name = variable.name
            print '\nResults for variable', name
            for key, item in vals:
                if key.startswith(name + '__'):
                    print item, key

if __name__ == '__main__':
        
    # mode = 'iso'
    # mode = 'sm'
    mode = 'pog'
    # mode = 'cp'
    # mode = 'mssm_signal' 
    # mode = 'mssm_control'


    friend_func = None
    
    int_lumi = lumi
        
    qcd_from_same_sign = True
    w_qcd_mssm_method = True
    r_qcd_os_ss = 1.17

    if mode == 'iso':
        qcd_from_same_sign = False
        w_qcd_mssm_method = False
        friend_func = None

    run_central = True
    add_ttbar_sys = False
    add_tes_sys = False


    analysis_dir = '/afs/cern.ch/user/s/steggema/work/analysis/CMSSW_9_4_4/src/CMGTools/H2TauTau/cfgPython/mt/MC_AAA/'

    total_weight = 'weight*abs(weight_gen)'
    # total_weight = 'weight * (1. - 0.0772790*(l2_gen_match == 5 && l2_decayMode==0) - 0.138582*(l2_gen_match == 5 && l2_decayMode==1) - 0.220793*(l2_gen_match == 5 && l2_decayMode==10) )' # Tau ID eff scale factor

    print total_weight

    cuts, mt_cut = prepareCuts(mode)

    variables = createVariables(mode)

    if run_central:
        sample_dict, hist_dict = createSamples(mode, analysis_dir, total_weight, qcd_from_same_sign, w_qcd_mssm_method, r_qcd_os_ss)
        makePlots(variables, cuts, total_weight, sample_dict, hist_dict, qcd_from_same_sign, w_qcd_mssm_method, mt_cut, friend_func, dc_postfix='', create_trees=False)

    if add_ttbar_sys:

        weight_ttbar_up = 'weight * gen_top_weight'

        sample_dict, hist_dict = createSamples(mode, analysis_dir, weight_ttbar_up, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None)

        sample_dict_ttbar = {'all_samples':[s for s in sample_dict['all_samples'] if s.name == 'TT']}

        makePlots(variables, cuts, weight_ttbar_up, sample_dict_ttbar, hist_dict={}, qcd_from_same_sign=False, w_qcd_mssm_method=False, mt_cut=mt_cut, friend_func=friend_func, dc_postfix='_CMS_htt_ttbarShape_13TeVUp', make_plots=False)

        weight_ttbar_down = 'weight / gen_top_weight'

        sample_dict, hist_dict = createSamples(mode, analysis_dir, weight_ttbar_up, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None)

        sample_dict_ttbar = {'all_samples':[s for s in sample_dict['all_samples'] if s.name == 'TT']}


        makePlots(variables, cuts, weight_ttbar_down, sample_dict_ttbar, hist_dict={}, qcd_from_same_sign=False, w_qcd_mssm_method=False, mt_cut=mt_cut, friend_func=friend_func, dc_postfix='_CMS_htt_ttbarShape_13TeVDown', make_plots=False)

    if add_tes_sys:
        tes_samples = ['ZTT', 'ZTTM10', 'HiggsGGH125', 'HiggsVBF125']

        analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitTESUp/'
        sample_dict, hist_dict = createSamples(mode, analysis_dir, total_weight, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None)
        sample_dict_tes = {'all_samples':[s for s in sample_dict['all_samples'] if s.name in tes_samples]}
        makePlots(variables, cuts, total_weight, sample_dict_tes, hist_dict={}, qcd_from_same_sign=False, w_qcd_mssm_method=False, mt_cut=mt_cut, friend_func=lambda f: f.replace('TESUp', 'TESUpMultiMVA'), dc_postfix='_CMS_scale_t_mt_13TeVUp', make_plots=False)

        analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitTESDown/'
        sample_dict, hist_dict = createSamples(mode, analysis_dir, total_weight, qcd_from_same_sign=False, w_qcd_mssm_method=False, r_qcd_os_ss=None)
        sample_dict_tes = {'all_samples':[s for s in sample_dict['all_samples'] if s.name in tes_samples]}

        makePlots(variables, cuts, total_weight, sample_dict_tes, hist_dict={}, qcd_from_same_sign=False, w_qcd_mssm_method=False, mt_cut=mt_cut, friend_func=lambda f: f.replace('TESDown', 'TESDownMultiMVA'), dc_postfix='_CMS_scale_t_mt_13TeVDown', make_plots=False)


