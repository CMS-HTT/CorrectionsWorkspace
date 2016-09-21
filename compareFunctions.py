#!/usr/bin/env python
import ROOT
import imp
import CombineHarvester.CombineTools.plotting as plot
wsptools = imp.load_source('wsptools', 'workspaceTools.py')
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

fin = ROOT.TFile('htt_scalefactors_v5.root')
w = fin.Get('w')


def Compare(w, output, fn1, fn2, bins, var, other_vars= {}, line_pos=None):
    label_vars = []
    for key, val in other_vars.iteritems():
        w.var(key).setVal(val)
        label_vars.append('%s=%g' % (key, val))
    h1 = w.function(fn1).createHistogram(fn1, w.var(var),
            ROOT.RooFit.Binning(*bins),
            ROOT.RooFit.Scaling(False)
        )
    h2 = w.function(fn2).createHistogram(fn2, w.var(var),
            ROOT.RooFit.Binning(*bins),
            ROOT.RooFit.Scaling(False)
        )
    canv = ROOT.TCanvas(output, output)
    pads = plot.TwoPadSplit(0.30, 0.01, 0.01)
    pads[0].cd()
    pads[0].SetGrid(1, 1)
    plot.Set(h1, LineColor=ROOT.kBlack, LineWidth=2)
    plot.Set(h1.GetYaxis(), Title='Efficiency')
    plot.Set(h2, LineColor=ROOT.kRed, LineWidth=2)

    for i in xrange(1, h1.GetNbinsX()+1):
        h1.SetBinError(i, 0.)
    for i in xrange(1, h2.GetNbinsX()+1):
        h2.SetBinError(i, 0.)
    h1.Draw('L')
    h2.Draw('LSAME')
    ratio = h1.Clone()
    ratio.Divide(h2)


    legend = ROOT.TLegend(0.18, 0.82, 0.6, 0.93, '', 'NBNDC')
    legend.AddEntry(h1, fn1, 'L')
    legend.AddEntry(h2, fn2, 'L')
    legend.Draw()
    print plot.GetPadYMax(pads[0])
    plot.FixTopRange(pads[0], plot.GetPadYMax(pads[0]), 0.25)
    plot.DrawTitle(pads[0], ','.join(label_vars), 1)

    line = ROOT.TLine()
    plot.Set(line, LineColor=12, LineStyle=4, LineWidth=2)
    if line_pos is not None:
        plot.DrawVerticalLine(pads[0], line, line_pos)

    pads[1].cd()
    pads[1].SetGrid(1, 1)
    ratio.Draw('L')
    plot.SetupTwoPadSplitAsRatio(
        pads, plot.GetAxisHist(
            pads[0]), plot.GetAxisHist(pads[1]), 'Ratio', True, 0.91, 1.09)
    if line_pos is not None:
        plot.DrawVerticalLine(pads[1], line, line_pos)
    canv.Print('.pdf')
    canv.Print('.png')

w.var('m_eta').setVal(1.3)
Compare(w, 'compare_kit_desy_m_trg_data_low_pt_eta_0p0', 'm_trg_data', 'm_trgIsoMu22_desy_data', bins=[200, 0, 50], var='m_pt', other_vars={'m_eta':0.0}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trg_data_low_pt_eta_0p9', 'm_trg_data', 'm_trgIsoMu22_desy_data', bins=[200, 0, 50], var='m_pt', other_vars={'m_eta':0.9}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trg_data_low_pt_eta_1p2', 'm_trg_data', 'm_trgIsoMu22_desy_data', bins=[200, 0, 50], var='m_pt', other_vars={'m_eta':1.2}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trg_data_low_pt_eta_2p1', 'm_trg_data', 'm_trgIsoMu22_desy_data', bins=[200, 0, 50], var='m_pt', other_vars={'m_eta':2.1}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trg_data_eta_0p0', 'm_trg_data', 'm_trgIsoMu22_desy_data', bins=[1000, 0, 1000], var='m_pt', other_vars={'m_eta':0.0}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trg_data_eta_0p9', 'm_trg_data', 'm_trgIsoMu22_desy_data', bins=[1000, 0, 1000], var='m_pt', other_vars={'m_eta':0.9}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trg_data_eta_1p2', 'm_trg_data', 'm_trgIsoMu22_desy_data', bins=[1000, 0, 1000], var='m_pt', other_vars={'m_eta':1.2}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trg_data_eta_2p1', 'm_trg_data', 'm_trgIsoMu22_desy_data', bins=[1000, 0, 1000], var='m_pt', other_vars={'m_eta':2.1}, line_pos=23.)

Compare(w, 'compare_kit_desy_m_trgOR_data_low_pt_eta_0p0', 'm_trgOR_data', 'm_trgIsoMu22orTkIsoMu22_desy_data', bins=[200, 0, 50], var='m_pt', other_vars={'m_eta':0.0}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trgOR_data_low_pt_eta_0p9', 'm_trgOR_data', 'm_trgIsoMu22orTkIsoMu22_desy_data', bins=[200, 0, 50], var='m_pt', other_vars={'m_eta':0.9}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trgOR_data_low_pt_eta_1p2', 'm_trgOR_data', 'm_trgIsoMu22orTkIsoMu22_desy_data', bins=[200, 0, 50], var='m_pt', other_vars={'m_eta':1.2}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trgOR_data_low_pt_eta_2p1', 'm_trgOR_data', 'm_trgIsoMu22orTkIsoMu22_desy_data', bins=[200, 0, 50], var='m_pt', other_vars={'m_eta':2.1}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trgOR_data_eta_0p0', 'm_trgOR_data', 'm_trgIsoMu22orTkIsoMu22_desy_data', bins=[1000, 0, 1000], var='m_pt', other_vars={'m_eta':0.0}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trgOR_data_eta_0p9', 'm_trgOR_data', 'm_trgIsoMu22orTkIsoMu22_desy_data', bins=[1000, 0, 1000], var='m_pt', other_vars={'m_eta':0.9}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trgOR_data_eta_1p2', 'm_trgOR_data', 'm_trgIsoMu22orTkIsoMu22_desy_data', bins=[1000, 0, 1000], var='m_pt', other_vars={'m_eta':1.2}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_trgOR_data_eta_2p1', 'm_trgOR_data', 'm_trgIsoMu22orTkIsoMu22_desy_data', bins=[1000, 0, 1000], var='m_pt', other_vars={'m_eta':2.1}, line_pos=23.)


Compare(w, 'compare_kit_desy_m_idiso_ratio_eta_0p0', 'm_idiso_ratio', 'm_idiso0p15_desy_ratio', bins=[200, 0, 200], var='m_pt', other_vars={'m_eta':0.0}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_idiso_ratio_eta_0p9', 'm_idiso_ratio', 'm_idiso0p15_desy_ratio', bins=[200, 0, 200], var='m_pt', other_vars={'m_eta':0.9}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_idiso_ratio_eta_1p2', 'm_idiso_ratio', 'm_idiso0p15_desy_ratio', bins=[200, 0, 200], var='m_pt', other_vars={'m_eta':1.2}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_idiso_ratio_eta_2p1', 'm_idiso_ratio', 'm_idiso0p15_desy_ratio', bins=[200, 0, 200], var='m_pt', other_vars={'m_eta':2.1}, line_pos=23.)

Compare(w, 'compare_kit_desy_e_trg_data_low_pt_eta_0p0', 'e_trg_data', 'e_trgEle25eta2p1WPTight_desy_data', bins=[200, 0, 50], var='e_pt', other_vars={'e_eta':0.0}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_trg_data_low_pt_eta_2p0', 'e_trg_data', 'e_trgEle25eta2p1WPTight_desy_data', bins=[200, 0, 50], var='e_pt', other_vars={'e_eta':2.0}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_trg_data_low_pt_eta_2p4', 'e_trg_data', 'e_trgEle25eta2p1WPTight_desy_data', bins=[200, 0, 50], var='e_pt', other_vars={'e_eta':2.4}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_trg_data_eta_0p0', 'e_trg_data', 'e_trgEle25eta2p1WPTight_desy_data', bins=[1000, 0, 1000], var='e_pt', other_vars={'e_eta':0.0}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_trg_data_eta_2p0', 'e_trg_data', 'e_trgEle25eta2p1WPTight_desy_data', bins=[1000, 0, 1000], var='e_pt', other_vars={'e_eta':2.0}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_trg_data_eta_2p4', 'e_trg_data', 'e_trgEle25eta2p1WPTight_desy_data', bins=[1000, 0, 1000], var='e_pt', other_vars={'e_eta':2.4}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_ratio_eta_0p0', 'e_idiso_ratio', 'e_idiso0p10_desy_ratio', bins=[200, 0, 200], var='e_pt', other_vars={'e_eta':0.0}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_ratio_eta_2p0', 'e_idiso_ratio', 'e_idiso0p10_desy_ratio', bins=[200, 0, 200], var='e_pt', other_vars={'e_eta':2.0}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_ratio_eta_2p4', 'e_idiso_ratio', 'e_idiso0p10_desy_ratio', bins=[200, 0, 200], var='e_pt', other_vars={'e_eta':2.4}, line_pos=26.)
# w.writeToFile('htt_scalefactors_v2.root')
# w.Delete()
