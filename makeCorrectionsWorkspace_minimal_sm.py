#!/usr/bin/env python
import ROOT
import imp
import json
from array import array
wsptools = imp.load_source('wsptools', 'workspaceTools.py')


def GetFromTFile(str):
    f = ROOT.TFile(str.split(':')[0])
    obj = f.Get(str.split(':')[1]).Clone()
    f.Close()
    return obj

# Boilerplate
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.RooWorkspace.imp = getattr(ROOT.RooWorkspace, 'import')
ROOT.TH1.AddDirectory(0)
ROOT.gROOT.LoadMacro("CrystalBallEfficiency.cxx+")

w = ROOT.RooWorkspace('w')


### DESY electron/muon tag and probe results
loc = 'inputs/LeptonEfficiencies'

desyHistsToWrap = [
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_IsoLt0p15_2016BtoH_eff.root',            'MC',   'm_idiso0p15_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_IsoLt0p15_2016BtoH_eff.root',            'Data', 'm_idiso0p15_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_IsoLt0p2_2016BtoH_eff.root',            'MC',   'm_idiso0p20_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_IsoLt0p2_2016BtoH_eff.root',            'Data', 'm_idiso0p20_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_antiisolated_Iso0p15to0p3_eff_rb.root',            'MC',   'm_idiso_aiso0p15to0p3_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_IdIso_antiisolated_Iso0p15to0p3_eff_rb.root',            'Data',   'm_idiso_aiso0p15to0p3_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p05to0p15_IdIso_eff.root',            'MC',   'm_idiso_aiso0p05to0p15_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p05to0p15_IdIso_eff.root',            'Data',   'm_idiso_aiso0p05to0p15_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p15to0p25_IdIso_eff.root',            'MC',   'm_idiso_aiso0p15to0p25_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p15to0p25_IdIso_eff.root',            'Data',   'm_idiso_aiso0p15to0p25_desy_data'),

    (loc+'/Muon/Run2016BtoH/Muon_IsoMu24_2016BtoH_eff.root',              'MC', 'm_trgIsoMu24_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_IsoMu24_2016BtoH_eff.root',              'Data', 'm_trgIsoMu24_desy_data'),

    (loc+'/Muon/Run2016BtoH/Muon_IsoMu24_OR_TkIsoMu24_2016BtoH_eff.root', 'MC', 'm_trgIsoMu24orTkIsoMu24_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_IsoMu24_OR_TkIsoMu24_2016BtoH_eff.root', 'Data', 'm_trgIsoMu24orTkIsoMu24_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p05to0p15_IsoMu24ORTkIsoMu24_eff_rb.root', 'MC', 'm_trgIsoMu24orTkIsoMu24_aiso0p05to0p15_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p05to0p15_IsoMu24ORTkIsoMu24_eff_rb.root', 'Data', 'm_trgIsoMu24orTkIsoMu24_aiso0p05to0p15_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p15to0p25_IsoMu24ORTkIsoMu24_eff_rb.root', 'MC', 'm_trgIsoMu24orTkIsoMu24_aiso0p15to0p25_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_antiisolated_0p15to0p25_IsoMu24ORTkIsoMu24_eff_rb.root', 'Data', 'm_trgIsoMu24orTkIsoMu24_aiso0p15to0p25_desy_data'),

    (loc+'/Muon/Run2016BtoH/Muon_Mu8leg_2016BtoH_eff.root',               'MC', 'm_trgMu8leg_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu8leg_2016BtoH_eff.root',               'Data', 'm_trgMu8leg_desy_data'),

    (loc+'/Muon/Run2016BtoH/Muon_Mu23leg_2016BtoH_eff.root',              'MC', 'm_trgMu23leg_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu23leg_2016BtoH_eff.root',              'Data', 'm_trgMu23leg_desy_data'),

    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_2016BtoH_eff.root',              'MC', 'm_trgMu19leg_eta2p1_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_2016BtoH_eff.root',              'Data', 'm_trgMu19leg_eta2p1_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p05to0p15_eff_rb.root',              'MC', 'm_trgMu19leg_eta2p1_aiso0p05to0p15_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p05to0p15_eff_rb.root',              'Data', 'm_trgMu19leg_eta2p1_aiso0p05to0p15_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p15to0p25_eff_rb.root',              'MC', 'm_trgMu19leg_eta2p1_aiso0p15to0p25_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p15to0p25_eff_rb.root',              'Data', 'm_trgMu19leg_eta2p1_aiso0p15to0p25_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p15to0p3_eff_rb.root',              'MC', 'm_trgMu19leg_eta2p1_aiso0p15to0p3_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu19leg_eta2p1_antiisolated_Iso0p15to0p3_eff_rb.root',              'Data', 'm_trgMu19leg_eta2p1_aiso0p15to0p3_desy_data'),

    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_eff.root',              'MC', 'm_trgMu22OR_eta2p1_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_eff.root',              'Data', 'm_trgMu22OR_eta2p1_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p05to0p15_eff_rb.root',              'MC', 'm_trgMu22OR_eta2p1_aiso0p05to0p15_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p05to0p15_eff_rb.root',              'Data', 'm_trgMu22OR_eta2p1_aiso0p05to0p15_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p15to0p25_eff_rb.root',              'MC', 'm_trgMu22OR_eta2p1_aiso0p15to0p25_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p15to0p25_eff_rb.root',              'Data', 'm_trgMu22OR_eta2p1_aiso0p15to0p25_desy_data'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p15to0p3_eff_rb.root',              'MC', 'm_trgMu22OR_eta2p1_aiso0p15to0p3_desy_mc'),
    (loc+'/Muon/Run2016BtoH/Muon_Mu22OR_eta2p1_antiisolated_Iso0p15to0p3_eff_rb.root',              'Data', 'm_trgMu22OR_eta2p1_aiso0p15to0p3_desy_data'),
]

for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])
for t in ['idiso0p15_desy', 'idiso0p20_desy', 'idiso_aiso0p15to0p3_desy', 'idiso_aiso0p05to0p15_desy', 'idiso_aiso0p15to0p25_desy', 'trgIsoMu24_desy', 'trgIsoMu24orTkIsoMu24_desy',    'trgIsoMu24orTkIsoMu24_aiso0p05to0p15_desy', 'trgIsoMu24orTkIsoMu24_aiso0p15to0p25_desy', 'trgMu8leg_desy', 'trgMu23leg_desy', 'trgMu19leg_eta2p1_desy', 'trgMu19leg_eta2p1_aiso0p05to0p15_desy', 'trgMu19leg_eta2p1_aiso0p15to0p25_desy', 'trgMu19leg_eta2p1_aiso0p15to0p3_desy', 'trgMu22OR_eta2p1_desy', 'trgMu22OR_eta2p1_aiso0p05to0p15_desy', 'trgMu22OR_eta2p1_aiso0p15to0p25_desy', 'trgMu22OR_eta2p1_aiso0p15to0p3_desy']:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))

desyHistsToWrap = [
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_IsoLt0p1_eff.root',          'MC',   'e_idiso0p1_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_IsoLt0p1_eff.root',          'Data', 'e_idiso0p1_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_IsoLt0p15_eff.root',          'MC',   'e_idiso0p15_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_IsoLt0p15_eff.root',          'Data', 'e_idiso0p15_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_antiisolated_0p05to0p15_IdIso_eff.root',          'MC',   'e_idiso_aiso0p05to0p15_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_antiisolated_0p05to0p15_IdIso_eff.root',          'Data', 'e_idiso_aiso0p05to0p15_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_antiisolated_0p10to0p20_IdIso_eff.root',          'MC',   'e_idiso_aiso0p1to0p2_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_antiisolated_0p10to0p20_IdIso_eff.root',          'Data', 'e_idiso_aiso0p1to0p2_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_antiisolated_Iso0p1to0p3_eff.root',          'MC',   'e_idiso_aiso0p1to0p3_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_IdIso_antiisolated_Iso0p1to0p3_eff.root',          'Data', 'e_idiso_aiso0p1to0p3_desy_data'),

    (loc+'/Electron/Run2016BtoH/Electron_Ele24_eff.root',          'MC',   'e_trgEle24_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_eff.root',          'Data', 'e_trgEle24_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p05to0p15_eff_rb.root',          'MC',   'e_trgEle24_aiso0p05to0p15_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p05to0p15_eff_rb.root',          'Data', 'e_trgEle24_aiso0p05to0p15_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p1to0p2_eff_rb.root',          'MC',   'e_trgEle24_aiso0p1to0p2_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p1to0p2_eff_rb.root',          'Data', 'e_trgEle24_aiso0p1to0p2_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p1to0p3_eff_rb.root',          'MC',   'e_trgEle24_aiso0p1to0p3_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele24_antiisolated_Iso0p1to0p3_eff_rb.root',          'Data', 'e_trgEle24_aiso0p1to0p3_desy_data'),

    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_eff.root',          'MC',   'e_trgEle25eta2p1WPTight_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_eff.root',          'Data', 'e_trgEle25eta2p1WPTight_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p05to0p15_eff_rb.root',          'MC',   'e_trgEle25eta2p1WPTight_aiso0p05to0p15_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p05to0p15_eff_rb.root',          'Data', 'e_trgEle25eta2p1WPTight_aiso0p05to0p15_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p1to0p2_eff_rb.root',          'MC',   'e_trgEle25eta2p1WPTight_aiso0p1to0p2_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p1to0p2_eff_rb.root',          'Data', 'e_trgEle25eta2p1WPTight_aiso0p1to0p2_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p1to0p3_eff_rb.root',          'MC',   'e_trgEle25eta2p1WPTight_aiso0p1to0p3_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele25WPTight_antiisolated_Iso0p1to0p3_eff_rb.root',          'Data', 'e_trgEle25eta2p1WPTight_aiso0p1to0p3_desy_data'),

    (loc+'/Electron/Run2016BtoH/Electron_Ele12leg_eff.root',           'MC', 'e_trgEle12leg_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele12leg_eff.root',           'Data', 'e_trgEle12leg_desy_data'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele23leg_eff.root',           'MC', 'e_trgEle23leg_desy_mc'),
    (loc+'/Electron/Run2016BtoH/Electron_Ele23leg_eff.root',           'Data', 'e_trgEle23leg_desy_data')
]

for task in desyHistsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          wsptools.ProcessDESYLeptonSFs(task[0], task[1], task[2]), name=task[2])

for t in ['idiso0p10_KITbins_desy', 'idiso0p1_desy', 'idiso0p15_desy', 'idiso_aiso0p05to0p15_desy', 'idiso_aiso0p1to0p2_desy', 'idiso_aiso0p1to0p3_desy', 'trgEle24_desy', 'trgEle24_aiso0p05to0p15_desy', 'trgEle24_aiso0p1to0p2_desy', 'trgEle24_aiso0p1to0p3_desy', 'trgEle25eta2p1WPTight_desy', 'trgEle25eta2p1WPTight_aiso0p05to0p15_desy', 'trgEle25eta2p1WPTight_aiso0p1to0p2_desy', 'trgEle25eta2p1WPTight_aiso0p1to0p3_desy', 'trgEle25eta2p1WPTight_KITbins_desy', 'trgEle12leg_desy', 'trgEle23leg_desy']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))


### Hadronic tau trigger efficiencies

with open('inputs/triggerSF-Moriond17/di-tau/fitresults_tt_moriond2017.json') as jsonfile:
    pars = json.load(jsonfile)
    for tautype in ['genuine', 'fake']:
        for iso in ['VLooseIso','LooseIso','MediumIso','TightIso','VTightIso','VVTightIso']:
            for dm in ['dm0', 'dm1', 'dm10']:
                label = '%s_%s_%s' % (tautype, iso, dm)
                x = pars['data_%s' % (label)]
                w.factory('CrystalBallEfficiency::t_%s_tt_data(t_pt[0],%g,%g,%g,%g,%g)' % (
                    label, x['m_{0}'], x['sigma'], x['alpha'], x['n'], x['norm']
                ))

                x = pars['mc_%s' % (label)]
                w.factory('CrystalBallEfficiency::t_%s_tt_mc(t_pt[0],%g,%g,%g,%g,%g)' % (
                    label, x['m_{0}'], x['sigma'], x['alpha'], x['n'], x['norm']
                ))
            label = '%s_%s' % (tautype, iso)
            wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                               't_%s_tt_data' % label, ['t_%s_dm0_tt_data' % label, 't_%s_dm1_tt_data' % label, 't_%s_dm10_tt_data' % label])
            wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                               't_%s_tt_mc' % label, ['t_%s_dm0_tt_mc' % label, 't_%s_dm1_tt_mc' % label, 't_%s_dm10_tt_mc' % label])
            w.factory('expr::t_%s_tt_ratio("@0/@1", t_%s_tt_data, t_%s_tt_mc)' % (label, label, label))


interpOrder = 1


tau_tt_file = ROOT.TFile('inputs/tauleg_of_di_tau_real_taus_skim_v2.root')
tau_tt_file_mc = ROOT.TFile('inputs/tauleg_of_di_tau_real_taus_skim_mc_v2.root')

prefix = {
    'genuine': 'lowmt_zmass_sub',
    'fake': 'highmt_os'
}

for tautype in ['genuine', 'fake']:
    for iso in ['TightIso']:
        for dm in ['dm0', 'dm1', 'dm10']:
            label = 'binned_%s_%s_%s' % (tautype, iso, dm)
            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_tt_file.Get('%s_%s_%s_HLT_MediumIso35_L1iso30/tau_pt' % (prefix[tautype], iso, dm))), name='t_%s_tt_data' % label)

            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_tt_file_mc.Get('%s_%s_%s_HLT_MediumIso35_L1iso30/tau_pt' % (prefix[tautype], iso, dm))), name='t_%s_tt_mc' % label)

            w.function('t_%s_tt_data' % label).setInterpolationOrder(interpOrder)
            w.function('t_%s_tt_mc' % label).setInterpolationOrder(interpOrder)


        label = 'binned_%s_%s' % (tautype, iso)
        wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                           't_%s_tt_data' % label, ['t_%s_dm0_tt_data' % label, 't_%s_dm1_tt_data' % label, 't_%s_dm10_tt_data' % label])
        wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                           't_%s_tt_mc' % label, ['t_%s_dm0_tt_mc' % label, 't_%s_dm1_tt_mc' % label, 't_%s_dm10_tt_mc' % label])
        w.factory('expr::t_%s_tt_ratio("@0/@1", t_%s_tt_data, t_%s_tt_mc)' % (label, label, label))

tau_mt_file = ROOT.TFile('inputs/triggerSF-Moriond17/mu-tau/trigger_sf_mt.root')
for tautype in ['genuine', 'fake']:
    for iso in ['NoIso',
                'VLooseIso',
                'LooseIso',
                'MediumIso',
                'TightIso',
                'VTightIso',
                'VVTightIso']:
        for region in ['barrel', 'endcap']:
            label = '%s_%s_%s' % (tautype, region, iso)

            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_mt_file.Get('data_%s' % label)), name='t_%s_mt_data' % label)
            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_mt_file.Get('mc_%s' % label)), name='t_%s_mt_mc' % label)

            w.function('t_%s_mt_data' % label).setInterpolationOrder(interpOrder)
            w.function('t_%s_mt_mc' % label).setInterpolationOrder(interpOrder)

            w.factory('expr::t_%s_mt_ratio("@0/@1", t_%s_mt_data, t_%s_mt_mc)' % (label, label, label))

        w.factory('expr::t_%s_%s_mt_ratio("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_mt_ratio, t_%s_endcap_%s_mt_ratio)' %
            (tautype, iso, tautype, iso, tautype, iso))
        w.factory('expr::t_%s_%s_mt_data("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_mt_data, t_%s_endcap_%s_mt_data)' %
            (tautype, iso, tautype, iso, tautype, iso))
        w.factory('expr::t_%s_%s_mt_mc("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_mt_mc, t_%s_endcap_%s_mt_mc)' %
            (tautype, iso, tautype, iso, tautype, iso))

tau_mt_file.Close()


tau_et_file = ROOT.TFile('inputs/triggerSF-Moriond17/ele-tau/trigger_sf_et.root')
for tautype in ['genuine', 'fake']:
    for iso in ['NoIso',
                'VLooseIso',
                'LooseIso',
                'MediumIso',
                'TightIso',
                'VTightIso',
                'VVTightIso']:
        for region in ['barrel', 'endcap']:
            label = '%s_%s_%s' % (tautype, region, iso)

            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_et_file.Get('data_%s_dm0' % label)), name='t_%s_dm0_et_data' % label)
            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_et_file.Get('data_%s_dm1' % label)), name='t_%s_dm1_et_data' % label)
            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_et_file.Get('data_%s_dm10' % label)), name='t_%s_dm10_et_data' % label)

            wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                               't_%s_et_data' % label, ['t_%s_dm0_et_data' % label, 't_%s_dm1_et_data' % label, 't_%s_dm10_et_data' % label])

            wsptools.SafeWrapHist(w, ['t_pt'], wsptools.TGraphAsymmErrorsToTH1DForTaus(
                tau_et_file.Get('mc_%s' % label)), name='t_%s_et_mc' % label)

            w.function('t_%s_dm0_et_data' % label).setInterpolationOrder(interpOrder)
            w.function('t_%s_dm1_et_data' % label).setInterpolationOrder(interpOrder)
            w.function('t_%s_dm10_et_data' % label).setInterpolationOrder(interpOrder)
            w.function('t_%s_et_mc' % label).setInterpolationOrder(interpOrder)

            w.factory('expr::t_%s_et_ratio("@0/@1", t_%s_et_data, t_%s_et_mc)' % (label, label, label))

        w.factory('expr::t_%s_%s_et_data("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_et_data, t_%s_endcap_%s_et_data)' %
            (tautype, iso, tautype, iso, tautype, iso))
        w.factory('expr::t_%s_%s_et_mc("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_et_mc, t_%s_endcap_%s_et_mc)' %
            (tautype, iso, tautype, iso, tautype, iso))
        w.factory('expr::t_%s_%s_et_ratio("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_et_ratio, t_%s_endcap_%s_et_ratio)' %
            (tautype, iso, tautype, iso, tautype, iso))


tau_et_file.Close()


w.importClassCode('CrystalBallEfficiency')

w.Print()


w.writeToFile('htt_scalefactors_sm_moriond_v2.root')
w.Delete()


fin = ROOT.TFile('htt_scalefactors_sm_moriond_v2.root')
w = fin.Get('w')

taus = [
    (50.0303226283    , -0.690436537219, 10),
    (59.5032264387    , -1.95157183364 ,  0),
    (43.1410575009    ,  0.801236923794,  1),
    (35.2404971103    ,  1.89180734956 ,  0),
    (45.5487299326    , -1.33507357888 ,  1),
    (49.3098431225    , -0.55660978639 ,  1),
    (24.3615004894    ,  0.786721853764,  1),
    (59.8846279899    , -0.132008199188,  0),
    (30.2513219915    , -1.56642180495 , 10),
    (31.4383629152    ,  1.61171893841 ,  1),
    (400.4383629152   ,  1.61171893841 ,  1),
    (500.4383629152   ,  1.61171893841 ,  1),
    (10000.4383629152 ,  1.61171893841 ,  1),
]

test_func1 = w.function("t_fake_VLooseIso_et_ratio").functor(ROOT.RooArgList(w.argSet("t_pt,t_eta,t_dm")))
test_func2 = w.function("t_fake_VLooseIso_et_data").functor(ROOT.RooArgList(w.argSet("t_pt,t_eta,t_dm")))
test_func3 = w.function("t_fake_VLooseIso_et_mc").functor(ROOT.RooArgList(w.argSet("t_pt,t_eta")))
# In the event loop need to pass an array of the argument:
for tau in taus:
    args = array('d', [tau[0], tau[1], tau[2]])
    print '%10.8f %10.8f  %10.8f' % (test_func2.eval(args), test_func3.eval(array('d', [tau[0], tau[1]])), test_func1.eval(args))


