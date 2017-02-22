#!/usr/bin/env python
import ROOT
import imp
import CombineHarvester.CombineTools.plotting as plot
wsptools = imp.load_source('wsptools', 'workspaceTools.py')
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
plot.ModTDRStyle()

fin = ROOT.TFile('htt_scalefactors_v16_3.root')
w = fin.Get('w')


def Compare(w, output, SFname, fn1, fn2, bins, var, other_vars= {}, line_pos=None, ylims=None):
    label_vars = []
    for key, val in other_vars.iteritems():
        w.var(key).setVal(val)
        name = key
        particle = ""
        if name=="e_eta":
		name="#eta(e)"
		particle = "(e)"
	if name=="m_eta":
		name="#eta(#mu)"
		particle = "(#mu)"
        label_vars.append('%s=%g' % (name, val))
    h1 = w.function(fn1).createHistogram(fn1, w.var(var),
            ROOT.RooFit.Binning(*bins),
            ROOT.RooFit.Scaling(False)
        )
    h2 = w.function(fn2).createHistogram(fn2, w.var(var),
            ROOT.RooFit.Binning(*bins),
            ROOT.RooFit.Scaling(False)
        )
    herr = h1.Clone()
    canv = ROOT.TCanvas(output, output)
    pads = plot.TwoPadSplit(0.30, 0.01, 0.01)
    pads[0].cd()
    pads[0].SetGrid(1, 1)
    plot.Set(h1, LineColor=ROOT.kBlack, LineWidth=2)
    plot.Set(herr, FillColor=18, MarkerSize=0)
    plot.Set(herr.GetYaxis(), Title='Scale Factor')
    plot.Set(herr.GetXaxis(), Title='p_{T}%s' % (particle))
    plot.Set(h2, LineColor=ROOT.kRed, LineWidth=2)

    for i in xrange(1, h1.GetNbinsX()+1):
        h1.SetBinError(i, 0.)
        herr.SetBinError(i, herr.GetBinContent(i)*0.02)
    for i in xrange(1, h2.GetNbinsX()+1):
        h2.SetBinError(i, 0.)
    herr.Draw('E3')
    h1.Draw('LSAME')
    h2.Draw('LSAME')
    ratio = h2.Clone()
    ratio.Divide(h1)
    ratioerr = herr.Clone()
    ratioerr.Divide(h1)


    #legend = ROOT.TLegend(0.18, 0.82, 0.6, 0.93, '', 'NBNDC')
    #legend.AddEntry(h1, 'KIT + 2% error band', 'L')
    #legend.AddEntry(h2, 'DESY', 'L')
    #legend.Draw()
    print plot.GetPadYMax(pads[0])
    #plot.FixTopRange(pads[0], 1.5, 0) #plot.GetPadYMax(pads[0]), 0.25)
    #plot.FixBothRanges(pads[0], 0.0, 0, 1.5, 0)
    if ylims==None:
        upperlim=plot.GetPadYMax(pads[0])
        if upperlim>1.2:
            upperlim=1.2
        plot.FixTopRange(pads[0], upperlim, 0.25)
    else:
        plot.FixBothRanges(pads[0], ylims[0], 0, ylims[1], 0)
    plot.DrawTitle(pads[0], SFname, 1)
    plot.DrawTitle(pads[0], ','.join(label_vars), 3)
    
    canv.Update()
    box = ROOT.TBox()
    box.SetFillColor(1)
    box.SetFillStyle(3004)
    box.DrawBox(bins[1], pads[0].GetUymin(), line_pos, pads[0].GetUymax())

    line = ROOT.TLine()
    plot.Set(line, LineColor=12, LineStyle=4, LineWidth=2)
    if line_pos is not None:
        #plot.DrawVerticalLine(pads[0], line, line_pos)
        line.DrawLine(line_pos, pads[0].GetUymin(), line_pos, pads[0].GetUymax())

    legend = ROOT.TLegend(0.18, 0.82, 0.6, 0.93, '', 'NBNDC')
    legend.AddEntry(h1, 'KIT + 2% error band', 'L')
    legend.AddEntry(h2, 'DESY', 'L')
    legend.Draw()

    pads[1].cd()
    pads[1].SetGrid(1, 1)
    ratioerr.Draw('E3')
    ratio.Draw('LSAME')
    plot.SetupTwoPadSplitAsRatio(
        pads, plot.GetAxisHist(
            pads[0]), plot.GetAxisHist(pads[1]), 'KIT/DESY', True, 0.91, 1.09)
    canv.Update()
    box.DrawBox(bins[1], pads[1].GetUymin(), line_pos, pads[1].GetUymax())
    if line_pos is not None:
        #plot.DrawVerticalLine(pads[1], line, line_pos)
        line.DrawLine(line_pos, pads[1].GetUymin(), line_pos, pads[1].GetUymax())
    canv.Print('.pdf')
    canv.Print('.png')

w.var('m_eta').setVal(1.3)

'''
Compare(w, 'compare_kit_desy_m_trg24_ratio_low_pt_eta_0p0', 'HLT IsoMu24', 'm_trg24_ratio', 'm_trgIsoMu24_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':0.0}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg24_ratio_low_pt_eta_1p0', 'HLT IsoMu24', 'm_trg24_ratio', 'm_trgIsoMu24_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':1.0}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg24_ratio_low_pt_eta_1p3', 'HLT IsoMu24', 'm_trg24_ratio', 'm_trgIsoMu24_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':1.3}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg24_ratio_low_pt_eta_2p2', 'HLT IsoMu24', 'm_trg24_ratio', 'm_trgIsoMu24_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':2.2}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg24_ratio_eta_0p0', 'HLT IsoMu24', 'm_trg24_ratio', 'm_trgIsoMu24_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':0.0}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg24_ratio_eta_1p0', 'HLT IsoMu24', 'm_trg24_ratio', 'm_trgIsoMu24_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.0}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg24_ratio_eta_1p3', 'HLT IsoMu24', 'm_trg24_ratio', 'm_trgIsoMu24_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.3}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg24_ratio_eta_2p2', 'HLT IsoMu24', 'm_trg24_ratio', 'm_trgIsoMu24_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':2.2}, line_pos=25., ylims=[0.8,1.1])

Compare(w, 'compare_kit_desy_m_trg24OR_ratio_low_pt_eta_0p0', 'HLT IsoMu24 || HLT IsoTkMu24', 'm_trg24OR_ratio', 'm_trgIsoMu24orTkIsoMu24_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':0.0}, line_pos=25., ylims=[0.8,1.2])
Compare(w, 'compare_kit_desy_m_trg24OR_ratio_low_pt_eta_1p0', 'HLT IsoMu24 || HLT IsoTkMu24', 'm_trg24OR_ratio', 'm_trgIsoMu24orTkIsoMu24_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':1.0}, line_pos=25., ylims=[0.8,1.2])
Compare(w, 'compare_kit_desy_m_trg24OR_ratio_low_pt_eta_1p3', 'HLT IsoMu24 || HLT IsoTkMu24', 'm_trg24OR_ratio', 'm_trgIsoMu24orTkIsoMu24_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':1.3}, line_pos=25., ylims=[0.9,1.1])
Compare(w, 'compare_kit_desy_m_trg24OR_ratio_low_pt_eta_2p2', 'HLT IsoMu24 || HLT IsoTkMu24', 'm_trg24OR_ratio', 'm_trgIsoMu24orTkIsoMu24_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':2.2}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg24OR_ratio_eta_0p0', 'HLT IsoMu24 || HLT IsoTkMu24', 'm_trg24OR_ratio', 'm_trgIsoMu24orTkIsoMu24_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':0.0}, line_pos=25., ylims=[0.8,1.2])
Compare(w, 'compare_kit_desy_m_trg24OR_ratio_eta_1p0', 'HLT IsoMu24 || HLT IsoTkMu24', 'm_trg24OR_ratio', 'm_trgIsoMu24orTkIsoMu24_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.0}, line_pos=25., ylims=[0.8,1.2])
Compare(w, 'compare_kit_desy_m_trg24OR_ratio_eta_1p3', 'HLT IsoMu24 || HLT IsoTkMu24', 'm_trg24OR_ratio', 'm_trgIsoMu24orTkIsoMu24_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.3}, line_pos=25., ylims=[0.9,1.1])
Compare(w, 'compare_kit_desy_m_trg24OR_ratio_eta_2p2', 'HLT IsoMu24 || HLT IsoTkMu24', 'm_trg24OR_ratio', 'm_trgIsoMu24orTkIsoMu24_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':2.2}, line_pos=25., ylims=[0.8,1.1])
'''
Compare(w, 'compare_kit_desy_m_trg22OR4_ratio_low_pt_eta_0p0', 'HLT IsoMu22OR4', 'm_trgOR4_ratio', 'm_trgMu22OR_eta2p1_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':0.0}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg22OR4_ratio_low_pt_eta_1p0', 'HLT IsoMu22OR4', 'm_trgOR4_ratio', 'm_trgMu22OR_eta2p1_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':1.0}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg22OR4_ratio_low_pt_eta_1p3', 'HLT IsoMu22OR4', 'm_trgOR4_ratio', 'm_trgMu22OR_eta2p1_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':1.3}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg22OR4_ratio_low_pt_eta_2p2', 'HLT IsoMu22OR4', 'm_trgOR4_ratio', 'm_trgMu22OR_eta2p1_desy_ratio', bins=[200, 20, 50], var='m_pt', other_vars={'m_eta':2.2}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg22OR4_ratio_eta_0p0', 'HLT IsoMu24', 'm_trgOR4_ratio', 'm_trgMu22OR_eta2p1_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':0.0}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg22OR4_ratio_eta_1p0', 'HLT IsoMu24', 'm_trgOR4_ratio', 'm_trgMu22OR_eta2p1_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.0}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg22OR4_ratio_eta_1p3', 'HLT IsoMu24', 'm_trgOR4_ratio', 'm_trgMu22OR_eta2p1_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.3}, line_pos=25., ylims=[0.8,1.1])
Compare(w, 'compare_kit_desy_m_trg22OR4_ratio_eta_2p2', 'HLT IsoMu24', 'm_trgOR4_ratio', 'm_trgMu22OR_eta2p1_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':2.2}, line_pos=25., ylims=[0.8,1.1])

Compare(w, 'compare_kit_desy_m_idiso_ratio_eta_0p0', 'muon IdIso', 'm_idiso_ratio', 'm_idiso0p15_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':0.0}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_idiso_ratio_eta_1p0', 'muon IdIso', 'm_idiso_ratio', 'm_idiso0p15_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.0}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_idiso_ratio_eta_1p3', 'muon IdIso', 'm_idiso_ratio', 'm_idiso0p15_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.3}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_idiso_ratio_eta_2p2', 'muon IdIso', 'm_idiso_ratio', 'm_idiso0p15_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':2.2}, line_pos=23.)

Compare(w, 'compare_kit_desy_m_idiso_singlefit_ratio_eta_0p0', 'muon IdIso', 'm_idiso_singlefit_ratio', 'm_idiso0p15_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':0.0}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_idiso_singlefit_ratio_eta_1p0', 'muon IdIso', 'm_idiso_singlefit_ratio', 'm_idiso0p15_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.0}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_idiso_singlefit_ratio_eta_1p3', 'muon IdIso', 'm_idiso_singlefit_ratio', 'm_idiso0p15_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.3}, line_pos=23.)
Compare(w, 'compare_kit_desy_m_idiso_singlefit_ratio_eta_2p2', 'muon IdIso', 'm_idiso_singlefit_ratio', 'm_idiso0p15_desy_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':2.2}, line_pos=23.)

Compare(w, 'compare_kit_kitsinglefit_m_idiso_ratio_eta_0p0', 'muon IdIso', 'm_idiso_ratio', 'm_idiso_singlefit_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':0.0}, line_pos=23.)
Compare(w, 'compare_kit_kitsinglefit_m_idiso_ratio_eta_1p0', 'muon IdIso', 'm_idiso_ratio', 'm_idiso_singlefit_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.0}, line_pos=23.)
Compare(w, 'compare_kit_kitsinglefit_m_idiso_ratio_eta_1p3', 'muon IdIso', 'm_idiso_ratio', 'm_idiso_singlefit_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':1.3}, line_pos=23.)
Compare(w, 'compare_kit_kitsinglefit_m_idiso_ratio_eta_2p2', 'muon IdIso', 'm_idiso_ratio', 'm_idiso_singlefit_ratio', bins=[250, 0, 250], var='m_pt', other_vars={'m_eta':2.2}, line_pos=23.)

Compare(w, 'compare_kit_desy_e_trg_ratio_low_pt_eta_0p0', 'HLT_Ele25eta2p1WPTight', 'e_DESYtagNonSC_trg_ratio', 'e_trgEle25eta2p1WPTight_KITbins_desy_ratio', bins=[200, 20, 50], var='e_pt', other_vars={'e_eta':0.0}, line_pos=26., ylims=[0.7,1.2])
Compare(w, 'compare_kit_desy_e_trg_ratio_low_pt_eta_1p2', 'HLT_Ele25eta2p1WPTight', 'e_DESYtagNonSC_trg_ratio', 'e_trgEle25eta2p1WPTight_KITbins_desy_ratio', bins=[200, 20, 50], var='e_pt', other_vars={'e_eta':1.2}, line_pos=26., ylims=[0.3,1.2])
Compare(w, 'compare_kit_desy_e_trg_ratio_low_pt_eta_1p5', 'HLT_Ele25eta2p1WPTight', 'e_DESYtagNonSC_trg_ratio', 'e_trgEle25eta2p1WPTight_KITbins_desy_ratio', bins=[200, 20, 50], var='e_pt', other_vars={'e_eta':1.5}, line_pos=26., ylims=[0.5,1.2])
Compare(w, 'compare_kit_desy_e_trg_ratio_low_pt_eta_2p0', 'HLT_Ele25eta2p1WPTight', 'e_DESYtagNonSC_trg_ratio', 'e_trgEle25eta2p1WPTight_KITbins_desy_ratio', bins=[200, 20, 50], var='e_pt', other_vars={'e_eta':2.0}, line_pos=26.)
#Compare(w, 'compare_kit_desy_e_trg_ratio_low_pt_eta_2p4', 'HLT_Ele25eta2p1WPTight', 'e_DESYtagNonSC_trg_ratio', 'e_trgEle25eta2p1WPTight_desy_ratio', bins=[200, 0, 50], var='e_pt', other_vars={'e_eta':2.4}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_trg_ratio_eta_0p0', 'HLT_Ele25eta2p1WPTight', 'e_DESYtagNonSC_trg_ratio', 'e_trgEle25eta2p1WPTight_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':0.0}, line_pos=26., ylims=[0.7,1.2])
Compare(w, 'compare_kit_desy_e_trg_ratio_eta_1p2', 'HLT_Ele25eta2p1WPTight', 'e_DESYtagNonSC_trg_ratio', 'e_trgEle25eta2p1WPTight_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':1.2}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_trg_ratio_eta_1p5', 'HLT_Ele25eta2p1WPTight', 'e_DESYtagNonSC_trg_ratio', 'e_trgEle25eta2p1WPTight_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':1.5}, line_pos=26., ylims=[0.5,1.2])
Compare(w, 'compare_kit_desy_e_trg_ratio_eta_2p0', 'HLT_Ele25eta2p1WPTight', 'e_DESYtagNonSC_trg_ratio', 'e_trgEle25eta2p1WPTight_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':2.0}, line_pos=26.)
#Compare(w, 'compare_kit_desy_e_trg_ratio_eta_2p4', 'HLT_Ele25eta2p1WPTight', 'e_DESYtagNonSC_trg_ratio', 'e_trgEle25eta2p1WPTight_desy_ratio', bins=[1000, 0, 1000], var='e_pt', other_vars={'e_eta':2.4}, line_pos=26.)

Compare(w, 'compare_kit_desy_e_idiso_ratio_eta_0p0', 'electron IdIso', 'e_DESYtagNonSC_idiso_ratio', 'e_idiso0p10_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':0.0}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_ratio_eta_1p2', 'electron IdIso', 'e_DESYtagNonSC_idiso_ratio', 'e_idiso0p10_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':1.2}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_ratio_eta_1p5', 'electron IdIso', 'e_DESYtagNonSC_idiso_ratio', 'e_idiso0p10_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':1.5}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_ratio_eta_2p0', 'electron IdIso', 'e_DESYtagNonSC_idiso_ratio', 'e_idiso0p10_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':2.0}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_ratio_eta_2p4', 'electron IdIso', 'e_DESYtagNonSC_idiso_ratio', 'e_idiso0p10_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':2.4}, line_pos=26.)

Compare(w, 'compare_kit_desy_e_idiso_singlefit_ratio_eta_0p0', 'electron IdIso', 'e_DESYtagNonSC_idiso_singlefit_ratio', 'e_idiso0p10_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':0.0}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_singlefit_ratio_eta_1p2', 'electron IdIso', 'e_DESYtagNonSC_idiso_singlefit_ratio', 'e_idiso0p10_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':1.2}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_singlefit_ratio_eta_1p5', 'electron IdIso', 'e_DESYtagNonSC_idiso_singlefit_ratio', 'e_idiso0p10_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':1.5}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_singlefit_ratio_eta_2p0', 'electron IdIso', 'e_DESYtagNonSC_idiso_singlefit_ratio', 'e_idiso0p10_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':2.0}, line_pos=26.)
Compare(w, 'compare_kit_desy_e_idiso_singlefit_ratio_eta_2p4', 'electron IdIso', 'e_DESYtagNonSC_idiso_singlefit_ratio', 'e_idiso0p10_KITbins_desy_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':2.4}, line_pos=26.)

Compare(w, 'compare_kit_kitsinglefit_e_idiso_ratio_eta_0p0', 'electron IdIso', 'e_DESYtagNonSC_idiso_ratio', 'e_DESYtagNonSC_idiso_singlefit_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':0.0}, line_pos=26.)
Compare(w, 'compare_kit_kitsinglefit_e_idiso_ratio_eta_1p2', 'electron IdIso', 'e_DESYtagNonSC_idiso_ratio', 'e_DESYtagNonSC_idiso_singlefit_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':1.2}, line_pos=26.)
Compare(w, 'compare_kit_kitsinglefit_e_idiso_ratio_eta_1p5', 'electron IdIso', 'e_DESYtagNonSC_idiso_ratio', 'e_DESYtagNonSC_idiso_singlefit_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':1.5}, line_pos=26.)
Compare(w, 'compare_kit_kitsinglefit_e_idiso_ratio_eta_2p0', 'electron IdIso', 'e_DESYtagNonSC_idiso_ratio', 'e_DESYtagNonSC_idiso_singlefit_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':2.0}, line_pos=26.)
Compare(w, 'compare_kit_kitsinglefit_e_idiso_ratio_eta_2p4', 'electron IdIso', 'e_DESYtagNonSC_idiso_ratio', 'e_DESYtagNonSC_idiso_singlefit_ratio', bins=[250, 0, 250], var='e_pt', other_vars={'e_eta':2.4}, line_pos=26.)
# w.writeToFile('htt_scalefactors_v2.root')
# w.Delete()
