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


tau_mt_file = ROOT.TFile('inputs/TauTriggerMoriond17/trigger_sf_mt.root')
for obj in [
            'genuine_barrel_NoIso',
            'genuine_barrel_VLooseIso',
            'genuine_barrel_LooseIso',
            'genuine_barrel_MediumIso',
            'genuine_barrel_TightIso',
            'genuine_barrel_VTightIso',
            'genuine_barrel_VVTightIso',
            'genuine_endcap_NoIso',
            'genuine_endcap_VLooseIso',
            'genuine_endcap_LooseIso',
            'genuine_endcap_MediumIso',
            'genuine_endcap_TightIso',
            'genuine_endcap_VTightIso',
            'genuine_endcap_VVTightIso',
            'fake_barrel_NoIso',
            'fake_barrel_VLooseIso',
            'fake_barrel_LooseIso',
            'fake_barrel_MediumIso',
            'fake_barrel_TightIso',
            'fake_barrel_VTightIso',
            'fake_barrel_VVTightIso',
            'fake_endcap_NoIso',
            'fake_endcap_VLooseIso',
            'fake_endcap_LooseIso',
            'fake_endcap_MediumIso',
            'fake_endcap_TightIso',
            'fake_endcap_VTightIso',
            'fake_endcap_VVTightIso'
           ]:
    wsptools.SafeWrapHist(w, ['t_pt'],
                          wsptools.TGraphAsymmErrorsToTH1DForTaus(tau_mt_file.Get('data_%s' % obj)), name='t_%s_mt_data' % obj)
    w.function('t_%s_mt_data' % obj).setInterpolationOrder(1)
    wsptools.SafeWrapHist(w, ['t_pt'],
                          wsptools.TGraphAsymmErrorsToTH1DForTaus(tau_mt_file.Get('mc_%s' % obj)), name='t_%s_mt_mc' % obj)
    w.function('t_%s_mt_mc' % obj).setInterpolationOrder(1)
    w.factory('expr::t_%s_mt_ratio("@0/@1", t_%s_mt_data, t_%s_mt_mc)' % (obj, obj, obj))
tau_mt_file.Close()


tau_et_file = ROOT.TFile('inputs/TauTriggerMoriond17/trigger_sf_et.root')
for obj in [
            'genuine_barrel_NoIso',
            'genuine_barrel_VLooseIso',
            'genuine_barrel_LooseIso',
            'genuine_barrel_MediumIso',
            'genuine_barrel_TightIso',
            'genuine_barrel_VTightIso',
            'genuine_barrel_VVTightIso',
            'genuine_endcap_NoIso',
            'genuine_endcap_VLooseIso',
            'genuine_endcap_LooseIso',
            'genuine_endcap_MediumIso',
            'genuine_endcap_TightIso',
            'genuine_endcap_VTightIso',
            'genuine_endcap_VVTightIso',
            'fake_barrel_NoIso',
            'fake_barrel_VLooseIso',
            'fake_barrel_LooseIso',
            'fake_barrel_MediumIso',
            'fake_barrel_TightIso',
            'fake_barrel_VTightIso',
            'fake_barrel_VVTightIso',
            'fake_endcap_NoIso',
            'fake_endcap_VLooseIso',
            'fake_endcap_LooseIso',
            'fake_endcap_MediumIso',
            'fake_endcap_TightIso',
            'fake_endcap_VTightIso',
            'fake_endcap_VVTightIso'
           ]:
    wsptools.SafeWrapHist(w, ['t_pt'],
                          wsptools.TGraphAsymmErrorsToTH1DForTaus(tau_et_file.Get('data_%s_dm0' % obj)), name='t_%s_dm0_et_data' % obj)
    w.function('t_%s_dm0_et_data' % obj).setInterpolationOrder(1)
    wsptools.SafeWrapHist(w, ['t_pt'],
                          wsptools.TGraphAsymmErrorsToTH1DForTaus(tau_et_file.Get('data_%s_dm1' % obj)), name='t_%s_dm1_et_data' % obj)
    w.function('t_%s_dm1_et_data' % obj).setInterpolationOrder(1)
    wsptools.SafeWrapHist(w, ['t_pt'],
                          wsptools.TGraphAsymmErrorsToTH1DForTaus(tau_et_file.Get('data_%s_dm10' % obj)), name='t_%s_dm10_et_data' % obj)
    w.function('t_%s_dm10_et_data' % obj).setInterpolationOrder(1)
    wsptools.SafeWrapHist(w, ['t_pt'],
                          wsptools.TGraphAsymmErrorsToTH1DForTaus(tau_et_file.Get('mc_%s' % obj)), name='t_%s_et_mc' % obj)
    w.function('t_%s_et_mc' % obj).setInterpolationOrder(1)
tau_et_file.Close()


w.importClassCode('CrystalBallEfficiency')

w.Print()
w.writeToFile('htt_scalefactors_sm_moriond_v1.root')
w.Delete()
