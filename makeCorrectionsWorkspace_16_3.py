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


### KIT electron/muon tag and probe results
loc = 'inputs/KIT/v16_3'

histsToWrap = [
    (loc+'/ZmmTP_Data_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',                    'm_id_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',              'm_id_mc'),
    (loc+'/ZmmTP_Data_Fits_IDIso_pt_eta_bins.root:IDIso_pt_eta_bins',                    'm_idiso_singlefit_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_IDIso_pt_eta_bins.root:IDIso_pt_eta_bins',              'm_idiso_singlefit_mc'),
    (loc+'/ZmmTP_Data_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                        'm_iso_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                  'm_iso_mc'),
    (loc+'/ZmmTP_Data_Fits_ID_pt_eta_finebins.root:ID_pt_eta_finebins',                    'm_id_finebins_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_ID_pt_eta_finebins.root:ID_pt_eta_finebins',              'm_id_finebins_mc'),
    (loc+'/ZmmTP_Data_Fits_Iso_pt_eta_finebins.root:Iso_pt_eta_finebins',                        'm_iso_finebins_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_Iso_pt_eta_finebins.root:Iso_pt_eta_finebins',                  'm_iso_finebins_mc'),
    (loc+'/ZmmTP_Data_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',                    'm_aiso1_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',              'm_aiso1_mc'),
    (loc+'/ZmmTP_Data_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',                    'm_aiso2_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',              'm_aiso2_mc'),
    (loc+'/ZmmTP_Data_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',                'm_trg_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',                'm_trg_mc'),
    #(loc+'/ZmmTP_Data_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',    'm_trg_aiso1_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',    'm_trg_aiso1_mc'),
    #(loc+'/ZmmTP_Data_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',    'm_trg_aiso2_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',    'm_trg_aiso2_mc'),
    #(loc+'/ZmmTP_Data_Fits_TrgOR_Iso_pt_eta_bins.root:TrgOR_Iso_pt_eta_bins',              'm_trgOR_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR_Iso_pt_eta_bins.root:TrgOR_Iso_pt_eta_bins',              'm_trgOR_mc'),
    #(loc+'/ZmmTP_Data_Fits_TrgOR_AIso1_pt_bins_inc_eta.root:TrgOR_AIso1_pt_bins_inc_eta',  'm_trgOR_aiso1_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR_AIso1_pt_bins_inc_eta.root:TrgOR_AIso1_pt_bins_inc_eta',  'm_trgOR_aiso1_mc'),
    #(loc+'/ZmmTP_Data_Fits_TrgOR_AIso2_pt_bins_inc_eta.root:TrgOR_AIso2_pt_bins_inc_eta',  'm_trgOR_aiso2_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR_AIso2_pt_bins_inc_eta.root:TrgOR_AIso2_pt_bins_inc_eta',  'm_trgOR_aiso2_mc'),
    #(loc+'/ZmmTP_Data_Fits_TrgOR3_Iso_pt_eta_bins.root:TrgOR3_Iso_pt_eta_bins',              'm_trgOR3_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR3_Iso_pt_eta_bins.root:TrgOR3_Iso_pt_eta_bins',              'm_trgOR3_mc'),
    (loc+'/ZmmTP_Data_Fits_Trg24_Iso_pt_eta_bins.root:Trg24_Iso_pt_eta_bins',                'm_trg24_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_Trg24_Iso_pt_eta_bins.root:Trg24_Iso_pt_eta_bins',                'm_trg24_mc'),
    (loc+'/ZmmTP_Data_Fits_Trg24OR_Iso_pt_eta_bins.root:Trg24OR_Iso_pt_eta_bins',                'm_trg24OR_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_Trg24OR_Iso_pt_eta_bins.root:Trg24OR_Iso_pt_eta_bins',                'm_trg24OR_mc'),
    #(loc+'/ZmmTP_Data_Fits_Trg24OR3_Iso_pt_eta_bins.root:Trg24OR3_Iso_pt_eta_bins',                'm_trg24OR3_data'),
    #(loc+'/ZmmTP_DYJetsToLL_Fits_Trg24OR3_Iso_pt_eta_bins.root:Trg24OR3_Iso_pt_eta_bins',                'm_trg24OR3_mc')
    (loc+'/ZmmTP_Data_Fits_TrgOR4_Iso_pt_eta_bins.root:TrgOR4_Iso_pt_eta_bins',                'm_trgOR4_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR4_Iso_pt_eta_bins.root:TrgOR4_Iso_pt_eta_bins',                'm_trgOR4_mc'),
    (loc+'/ZmmTP_Data_Fits_TrgOR4_AIso1_pt_bins_inc_eta.root:TrgOR4_AIso1_pt_bins_inc_eta',    'm_trgOR4_aiso1_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR4_AIso1_pt_bins_inc_eta.root:TrgOR4_AIso1_pt_bins_inc_eta',    'm_trgOR4_aiso1_mc'),
    (loc+'/ZmmTP_Data_Fits_TrgOR4_AIso2_pt_bins_inc_eta.root:TrgOR4_AIso2_pt_bins_inc_eta',    'm_trgOR4_aiso2_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR4_AIso2_pt_bins_inc_eta.root:TrgOR4_AIso2_pt_bins_inc_eta',    'm_trgOR4_aiso2_mc'),
    (loc+'/ZmmTP_Data_Fits_TrgOR5_Iso_pt_eta_bins.root:TrgOR5_Iso_pt_eta_bins',                'm_trgOR5_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR5_Iso_pt_eta_bins.root:TrgOR5_Iso_pt_eta_bins',                'm_trgOR5_mc'),
    (loc+'/ZmmTP_Data_Fits_TrgOR5_AIso1_pt_bins_inc_eta.root:TrgOR5_AIso1_pt_bins_inc_eta',    'm_trgOR5_aiso1_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR5_AIso1_pt_bins_inc_eta.root:TrgOR5_AIso1_pt_bins_inc_eta',    'm_trgOR5_aiso1_mc'),
    (loc+'/ZmmTP_Data_Fits_TrgOR5_AIso2_pt_bins_inc_eta.root:TrgOR5_AIso2_pt_bins_inc_eta',    'm_trgOR5_aiso2_data'),
    (loc+'/ZmmTP_DYJetsToLL_Fits_TrgOR5_AIso2_pt_bins_inc_eta.root:TrgOR5_AIso2_pt_bins_inc_eta',    'm_trgOR5_aiso2_mc')
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['m_pt', 'expr::m_abs_eta("TMath::Abs(@0)",m_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])


wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_data', ['m_iso_data', 'm_aiso1_data', 'm_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_iso_binned_mc', ['m_iso_mc', 'm_aiso1_mc', 'm_aiso2_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_iso_finebins_binned_data', ['m_iso_finebins_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_iso_finebins_binned_mc', ['m_iso_finebins_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_trg_binned_data', ['m_trg_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_trg_binned_mc', ['m_trg_mc'])
'''
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR_binned_data', ['m_trgOR_data', 'm_trgOR_aiso1_data', 'm_trgOR_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR_binned_mc', ['m_trgOR_mc', 'm_trgOR_aiso1_mc', 'm_trgOR_aiso2_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_trgOR3_binned_data', ['m_trgOR3_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_trgOR3_binned_mc', ['m_trgOR3_mc'])
'''
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_trg24_binned_data', ['m_trg24_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_trg24_binned_mc', ['m_trg24_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_trg24OR_binned_data', ['m_trg24OR_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_trg24OR_binned_mc', ['m_trg24OR_mc'])
'''
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_trg24OR3_binned_data', ['m_trg24OR3_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15],
                                   'm_trg24OR3_binned_mc', ['m_trg24OR3_mc'])
'''
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR4_binned_data', ['m_trgOR4_data', 'm_trgOR4_aiso1_data', 'm_trgOR4_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR4_binned_mc', ['m_trgOR4_mc', 'm_trgOR4_aiso1_mc', 'm_trgOR4_aiso2_mc'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR5_binned_data', ['m_trgOR5_data', 'm_trgOR5_aiso1_data', 'm_trgOR5_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'm_iso', [0., 0.15, 0.25, 0.50],
                                   'm_trgOR5_binned_mc', ['m_trgOR5_mc', 'm_trgOR5_aiso1_mc', 'm_trgOR5_aiso2_mc'])


for t in ['id', 'id_finebins', 'idiso_singlefit', 'iso', 'aiso1', 'aiso2', 'iso_binned', 'iso_finebins', 'iso_finebins_binned', 'trg', 'trg_binned', 'trg24', 'trg24_binned', 'trg24OR', 'trg24OR_binned', 'trgOR4', 'trgOR4_aiso1', 'trgOR4_aiso2', 'trgOR4_binned', 'trgOR5', 'trgOR5_aiso1', 'trgOR5_aiso2', 'trgOR5_binned']:
    w.factory('expr::m_%s_ratio("@0/@1", m_%s_data, m_%s_mc)' % (t, t, t))

for t in ['data', 'mc', 'ratio']:
    w.factory('expr::m_idiso_%s("@0*@1", m_id_%s, m_iso_%s)' % (t, t, t))
    w.factory('expr::m_idiso_finebins_%s("@0*@1", m_id_finebins_%s, m_iso_finebins_%s)' % (t, t, t))

loc = 'inputs/KIT/v16_3'

histsToWrap = [
    (loc+'/ZeeTP_Data_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',                          'e_id_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_ID_pt_eta_bins.root:ID_pt_eta_bins',                    'e_id_mc'),
    (loc+'/ZeeTP_Data_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                        'e_iso_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Iso_pt_eta_bins.root:Iso_pt_eta_bins',                  'e_iso_mc'),
    (loc+'/ZeeTP_Data_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',                    'e_aiso1_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_AIso1_pt_eta_bins.root:AIso1_pt_eta_bins',              'e_aiso1_mc'),
    (loc+'/ZeeTP_Data_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',                    'e_aiso2_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_AIso2_pt_eta_bins.root:AIso2_pt_eta_bins',              'e_aiso2_mc'),
    (loc+'/ZeeTP_Data_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',                'e_trg_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Trg_Iso_pt_eta_bins.root:Trg_Iso_pt_eta_bins',                'e_trg_mc'),
    (loc+'/ZeeTP_Data_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',    'e_trg_aiso1_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Trg_AIso1_pt_bins_inc_eta.root:Trg_AIso1_pt_bins_inc_eta',    'e_trg_aiso1_mc'),
    (loc+'/ZeeTP_Data_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',    'e_trg_aiso2_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_Trg_AIso2_pt_bins_inc_eta.root:Trg_AIso2_pt_bins_inc_eta',    'e_trg_aiso2_mc'),
    (loc+'/ZeeTP_Data_Fits_TrgOR_Iso_pt_eta_bins.root:TrgOR_Iso_pt_eta_bins',                'e_trgOR_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_TrgOR_Iso_pt_eta_bins.root:TrgOR_Iso_pt_eta_bins',                'e_trgOR_mc'),
    (loc+'/ZeeTP_Data_Fits_TrgOR_AIso1_pt_bins_inc_eta.root:TrgOR_AIso1_pt_bins_inc_eta',    'e_trgOR_aiso1_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_TrgOR_AIso1_pt_bins_inc_eta.root:TrgOR_AIso1_pt_bins_inc_eta',    'e_trgOR_aiso1_mc'),
    (loc+'/ZeeTP_Data_Fits_TrgOR_AIso2_pt_bins_inc_eta.root:TrgOR_AIso2_pt_bins_inc_eta',    'e_trgOR_aiso2_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_TrgOR_AIso2_pt_bins_inc_eta.root:TrgOR_AIso2_pt_bins_inc_eta',    'e_trgOR_aiso2_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27_Iso_pt_eta_bins.root:Trg27_Iso_pt_eta_bins',                'e_trg27_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27_Iso_pt_eta_bins.root:Trg27_Iso_pt_eta_bins',                'e_trg27_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27_AIso1_pt_bins_inc_eta.root:Trg27_AIso1_pt_bins_inc_eta',    'e_trg27_aiso1_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27_AIso1_pt_bins_inc_eta.root:Trg27_AIso1_pt_bins_inc_eta',    'e_trg27_aiso1_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27_AIso2_pt_bins_inc_eta.root:Trg27_AIso2_pt_bins_inc_eta',    'e_trg27_aiso2_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27_AIso2_pt_bins_inc_eta.root:Trg27_AIso2_pt_bins_inc_eta',    'e_trg27_aiso2_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27OR_Iso_pt_eta_bins.root:Trg27OR_Iso_pt_eta_bins',                'e_trg27OR_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27OR_Iso_pt_eta_bins.root:Trg27OR_Iso_pt_eta_bins',                'e_trg27OR_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27OR_AIso1_pt_bins_inc_eta.root:Trg27OR_AIso1_pt_bins_inc_eta',    'e_trg27OR_aiso1_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27OR_AIso1_pt_bins_inc_eta.root:Trg27OR_AIso1_pt_bins_inc_eta',    'e_trg27OR_aiso1_mc'),
    #(loc+'/ZeeTP_Data_Fits_Trg27OR_AIso2_pt_bins_inc_eta.root:Trg27OR_AIso2_pt_bins_inc_eta',    'e_trg27OR_aiso2_data'),
    #(loc+'/ZeeTP_DYJetsToLL_Fits_Trg27OR_AIso2_pt_bins_inc_eta.root:Trg27OR_AIso2_pt_bins_inc_eta',    'e_trg27OR_aiso2_mc')
    (loc+'/ZeeTP_Data_Fits_DESYtag_ID_pt_eta_bins.root:DESYtag_ID_pt_eta_bins',                          'e_DESYtag_id_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtag_ID_pt_eta_bins.root:DESYtag_ID_pt_eta_bins',                    'e_DESYtag_id_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtag_Iso_pt_eta_bins.root:DESYtag_Iso_pt_eta_bins',                        'e_DESYtag_iso_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtag_Iso_pt_eta_bins.root:DESYtag_Iso_pt_eta_bins',                  'e_DESYtag_iso_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtag_Trg_Iso_pt_eta_bins.root:DESYtag_Trg_Iso_pt_eta_bins',                'e_DESYtag_trg_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtag_Trg_Iso_pt_eta_bins.root:DESYtag_Trg_Iso_pt_eta_bins',                'e_DESYtag_trg_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtagNonSC_ID_pt_eta_bins.root:DESYtagNonSC_ID_pt_eta_bins',                          'e_DESYtagNonSC_id_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtagNonSC_ID_pt_eta_bins.root:DESYtagNonSC_ID_pt_eta_bins',                    'e_DESYtagNonSC_id_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtagNonSC_IDIso_pt_eta_bins.root:DESYtagNonSC_IDIso_pt_eta_bins',                          'e_DESYtagNonSC_idiso_singlefit_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtagNonSC_IDIso_pt_eta_bins.root:DESYtagNonSC_IDIso_pt_eta_bins',                    'e_DESYtagNonSC_idiso_singlefit_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtagNonSC_Iso_pt_eta_bins.root:DESYtagNonSC_Iso_pt_eta_bins',                        'e_DESYtagNonSC_iso_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtagNonSC_Iso_pt_eta_bins.root:DESYtagNonSC_Iso_pt_eta_bins',                  'e_DESYtagNonSC_iso_mc'),
    (loc+'/ZeeTP_Data_Fits_DESYtagNonSC_Trg_Iso_pt_eta_bins.root:DESYtagNonSC_Trg_Iso_pt_eta_bins',                'e_DESYtagNonSC_trg_data'),
    (loc+'/ZeeTP_DYJetsToLL_Fits_DESYtagNonSC_Trg_Iso_pt_eta_bins.root:DESYtagNonSC_Trg_Iso_pt_eta_bins',                'e_DESYtagNonSC_trg_mc'),
    
]

for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['e_pt', 'expr::e_abs_eta("TMath::Abs(@0)",e_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])


wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_iso_binned_data', ['e_iso_data', 'e_aiso1_data', 'e_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_iso_binned_mc', ['e_iso_mc', 'e_aiso1_mc', 'e_aiso2_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg_binned_data', ['e_trg_data', 'e_trg_aiso1_data', 'e_trg_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg_binned_mc', ['e_trg_mc', 'e_trg_aiso1_mc', 'e_trg_aiso2_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trgOR_binned_data', ['e_trgOR_data', 'e_trgOR_aiso1_data', 'e_trgOR_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trgOR_binned_mc', ['e_trgOR_mc', 'e_trgOR_aiso1_mc', 'e_trgOR_aiso2_mc'])
'''
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg27_binned_data', ['e_trg27_data', 'e_trg27_aiso1_data', 'e_trg27_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg27_binned_mc', ['e_trg27_mc', 'e_trg27_aiso1_mc', 'e_trg27_aiso2_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg27OR_binned_data', ['e_trg27OR_data', 'e_trg27OR_aiso1_data', 'e_trg27OR_aiso2_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10, 0.20, 0.50],
                                   'e_trg27OR_binned_mc', ['e_trg27OR_mc', 'e_trg27OR_aiso1_mc', 'e_trg27OR_aiso2_mc'])
'''
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtag_iso_binned_data', ['e_DESYtag_iso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_DESYtag_iso', [0., 0.10],
                                   'e_DESYtag_iso_binned_mc', ['e_DESYtag_iso_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtag_trg_binned_data', ['e_DESYtag_trg_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtag_trg_binned_mc', ['e_DESYtag_trg_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtag_trgOR_binned_data', ['e_DESYtag_trgOR_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtag_trgOR_binned_mc', ['e_DESYtag_trgOR_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtagNonSC_iso_binned_data', ['e_DESYtagNonSC_iso_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtagNonSC_iso_binned_mc', ['e_DESYtagNonSC_iso_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtagNonSC_trg_binned_data', ['e_DESYtagNonSC_trg_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtagNonSC_trg_binned_mc', ['e_DESYtagNonSC_trg_mc'])

wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtagNonSC_trgOR_binned_data', ['e_DESYtagNonSC_trgOR_data'])
wsptools.MakeBinnedCategoryFuncMap(w, 'e_iso', [0., 0.10],
                                   'e_DESYtagNonSC_trgOR_binned_mc', ['e_DESYtagNonSC_trgOR_mc'])


for t in ['id', 'iso', 'aiso1', 'aiso2', 'iso_binned', 'trg', 'trg_aiso1', 'trg_aiso2', 'trg_binned', 'trgOR', 'trgOR_aiso1', 'trgOR_aiso2', 'trgOR_binned', 'DESYtag_id', 'DESYtag_iso', 'DESYtag_iso_binned', 'DESYtag_trg', 'DESYtag_trg_binned', 'DESYtag_trgOR', 'DESYtag_trgOR_binned', 'DESYtagNonSC_id', 'DESYtagNonSC_idiso_singlefit', 'DESYtagNonSC_iso', 'DESYtagNonSC_iso_binned', 'DESYtagNonSC_trg', 'DESYtagNonSC_trg_binned', 'DESYtagNonSC_trgOR', 'DESYtagNonSC_trgOR_binned']:
    w.factory('expr::e_%s_ratio("@0/@1", e_%s_data, e_%s_mc)' % (t, t, t))

for t in ['data', 'mc', 'ratio']:
    w.factory('expr::e_idiso_%s("@0*@1", e_id_%s, e_iso_%s)' % (t, t, t))
    w.factory('expr::e_DESYtag_idiso_%s("@0*@1", e_DESYtag_id_%s, e_DESYtag_iso_%s)' % (t, t, t))
    w.factory('expr::e_DESYtagNonSC_idiso_%s("@0*@1", e_DESYtagNonSC_id_%s, e_DESYtagNonSC_iso_%s)' % (t, t, t))

### Muon tracking efficiency scale factor from the muon POG
loc = 'inputs/MuonPOG'

muon_trk_eff_hist = wsptools.TGraphAsymmErrorsToTH1D(GetFromTFile(loc+'/Tracking_EfficienciesAndSF_BCDEFGH.root:ratio_eff_eta3_dr030e030_corr'))
wsptools.SafeWrapHist(w, ['m_eta'], muon_trk_eff_hist, name='m_trk_ratio')

### Electron tracking efficiency scale factor from the egamma POG
loc = 'inputs/EGammaPOG'

electron_trk_eff_hist = GetFromTFile(loc+'/egammaEffi.txt_EGM2D.root:EGamma_SF2D')
wsptools.SafeWrapHist(w, ['e_eta','e_pt'], electron_trk_eff_hist, name='e_trk_ratio')


### DESY electron/muon tag and probe results
loc = 'inputs/LeptonEfficiencies'
loc2 = 'inputs/DESYsyncSF'

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
    (loc2+'/Electron_IdIso_IsoLt0p1_2016BtoH_eff.root',          'MC',   'e_idiso0p10_KITbins_desy_mc'),
    (loc2+'/Electron_IdIso_IsoLt0p1_2016BtoH_eff.root',          'Data', 'e_idiso0p10_KITbins_desy_data'),
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
    
    (loc2+'/Electron_Ele25_eta2p1_WPTight_2016BtoH_eff.root', 'MC', 'e_trgEle25eta2p1WPTight_KITbins_desy_mc'),
    (loc2+'/Electron_Ele25_eta2p1_WPTight_2016BtoH_eff.root', 'Data', 'e_trgEle25eta2p1WPTight_KITbins_desy_data'),
    
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

### KIT tau ID scale factors
loc = 'inputs/KIT/tau_id_sfs_2016.root:'
histsToWrap = [
    (loc + 'mva_m_dm0_pt30', 't_iso_mva_m_dm0_pt30_sf'),
    (loc + 'mva_m_dm1_pt30', 't_iso_mva_m_dm1_pt30_sf'),
    (loc + 'mva_m_dm10_pt30', 't_iso_mva_m_dm10_pt30_sf'),
    (loc + 'mva_t_dm0_pt40_eta2p1', 't_iso_mva_t_dm0_pt40_eta2p1_sf'),
    (loc + 'mva_t_dm1_pt40_eta2p1', 't_iso_mva_t_dm1_pt40_eta2p1_sf'),
    (loc + 'mva_t_dm10_pt40_eta2p1', 't_iso_mva_t_dm10_pt40_eta2p1_sf'),
]
for task in histsToWrap:
    wsptools.SafeWrapHist(w, ['t_pt', 'expr::t_abs_eta("TMath::Abs(@0)",t_eta[0])'],
                          GetFromTFile(task[0]), name=task[1])

wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                   't_iso_mva_m_pt30_sf', ['t_iso_mva_m_dm0_pt30_sf', 't_iso_mva_m_dm1_pt30_sf', 't_iso_mva_m_dm10_pt30_sf'])

wsptools.MakeBinnedCategoryFuncMap(w, 't_dm', [-0.5, 0.5, 9.5, 10.5],
                                   't_iso_mva_t_pt40_eta2p1_sf', ['t_iso_mva_t_dm0_pt40_eta2p1_sf', 't_iso_mva_t_dm1_pt40_eta2p1_sf', 't_iso_mva_t_dm10_pt40_eta2p1_sf'])


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

### LO DYJetsToLL Z mass vs pT correction
wsptools.SafeWrapHist(w, ['z_gen_mass', 'z_gen_pt'],
                      GetFromTFile('inputs/zpt_weights_2016.root:zptmass_histo'), name='zpt_weight')

w.importClassCode('CrystalBallEfficiency')

w.Print()
w.writeToFile('htt_scalefactors_v16_3.root')
w.Delete()
