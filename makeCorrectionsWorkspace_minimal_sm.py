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


# ### Hadronic tau trigger efficiencies
# loc = 'inputs/triggerSF/di-tau'

# with open(loc+'/real_taus_cumulative.json') as jsonfile:
#     pars = json.load(jsonfile)
#     for wp in pars:
#         x = pars[wp]
#         w.factory('CrystalBallEfficiency::t_trg%s_data(t_pt[0],%g,%g,%g,%g,%g)' % (
#                 wp, x['m_{0}'], x['sigma'], x['alpha'], x['n'], x['norm']
#             ))

# with open(loc+'/same_sign_cumulative.json') as jsonfile:
#     pars = json.load(jsonfile)
#     for wp in pars:
#         x = pars[wp]
#         w.factory('CrystalBallEfficiency::t_trg%sSS_data(t_pt[0],%g,%g,%g,%g,%g)' % (
#                 wp, x['m_{0}'], x['sigma'], x['alpha'], x['n'], x['norm']
#             ))
interpOrder = 1

tau_mt_file = ROOT.TFile('inputs/TauTriggerMoriond17/trigger_sf_mt.root')
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
        fn = w.factory('expr::t_%s_%s_mt_ratio("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_mt_ratio, t_%s_endcap_%s_mt_ratio)' %
            (tautype, iso, tautype, iso, tautype, iso))

tau_mt_file.Close()


tau_et_file = ROOT.TFile('inputs/TauTriggerMoriond17/trigger_sf_et.root')
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

        fn = w.factory('expr::t_%s_%s_et_ratio("TMath::Abs(@0) < 1.5 ? @1 : @2", t_eta[0], t_%s_barrel_%s_et_ratio, t_%s_endcap_%s_et_ratio)' %
            (tautype, iso, tautype, iso, tautype, iso))


    # wsptools.SafeWrapHist(w, ['t_pt'],
    #                       wsptools.TGraphAsymmErrorsToTH1DForTaus(tau_et_file.Get('data_%s_dm0' % obj)), name='t_%s_dm0_et_data' % obj)
    # w.function('t_%s_dm0_et_data' % obj).setInterpolationOrder(1)
    # wsptools.SafeWrapHist(w, ['t_pt'],
    #                       wsptools.TGraphAsymmErrorsToTH1DForTaus(tau_et_file.Get('data_%s_dm1' % obj)), name='t_%s_dm1_et_data' % obj)
    # w.function('t_%s_dm1_et_data' % obj).setInterpolationOrder(1)
    # wsptools.SafeWrapHist(w, ['t_pt'],
    #                       wsptools.TGraphAsymmErrorsToTH1DForTaus(tau_et_file.Get('data_%s_dm10' % obj)), name='t_%s_dm10_et_data' % obj)
    # w.function('t_%s_dm10_et_data' % obj).setInterpolationOrder(1)
    # wsptools.SafeWrapHist(w, ['t_pt'],
    #                       wsptools.TGraphAsymmErrorsToTH1DForTaus(tau_et_file.Get('mc_%s' % obj)), name='t_%s_et_mc' % obj)
    # w.function('t_%s_et_mc' % obj).setInterpolationOrder(1)
tau_et_file.Close()


w.importClassCode('CrystalBallEfficiency')

w.Print()

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

test_func = w.function("t_genuine_VLooseIso_et_ratio").functor(ROOT.RooArgList(w.argSet("t_pt,t_eta,t_dm")))
# In the event loop need to pass an array of the argument:

for tau in taus:
    print test_func.eval(array('d', [tau[0], tau[1], tau[2]]))

w.writeToFile('htt_scalefactors_sm_moriond_v1.root')
w.Delete()
