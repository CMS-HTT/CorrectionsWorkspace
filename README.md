# Correction factors

**UPDATES**:
 - 21/09, htt_scalefactors_v5.root
   * Updated electron and muon trigger functions from DESY to use the fine-binned variants that are now aligned with the offline pT cuts used in the MSSM analysis.
 - 16/09, htt_scalefactors_v5.root
   * Fixed bug in `m_trgOR_data` and `m_trgOR_binned_data` - these were inadvertently giving the efficiencies of the IsoMu22 trigger, not the OR with the IsoTkMu22 trigger.
   * The muon ID efficiencies are now measured using the generalTracks collection as probes, to be in-line with what is done by the MuonPOG. However the efficiencies for pT < 20 GeV are still made with the tracker muons as probes, as the purity in the fail region is not high enough to use the tracks. These low pT scale factors may therefore be updated in the future.
   * Added muon trigger efficiencies for the `HLT_IsoMu19_eta2p1_LooseIsoPFTau20` and `HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1` cross triggers. For the former, another object in the event is required to have fired the tau part of the L1 seed as part of the denominator selection.
   * Added trigger efficiencies for the e-mu cross triggers measured by the DESY group.
   * Added updated LO DYJetsToLL Z pT vs mass weights

## Producing the workspace
Clone this repository and initialise the other repositories which are handled as git submodules:

    git clone https://github.com/CMS-HTT/CorrectionsWorkspace.git
    cd CorrectionsWorkspace
    git submodule update --init

The workspace is produced by running the following script:

    python makeCorrectionsWorkspace.py

The contents of the output can be inspected with:

    root -l htt_scalefactors_v5.root
    w->Print()
    # See more detail on the evaluation of a particular object:
    w->function("m_id_ratio")->Print("tree")

## Available corrections

Each name here corresponds to a RooFit function object in the workspace. See below for usage.

### Muons

 - `m_id_data` and `m_id_mc`: *double Voigtian* signal pdf, *RooCMSShape* background pdf
    * Probe denominator: Tracks unpacked from the PFCandidates, `pt > 20` and `abs(eta) < 2.4`. For `pt < 20` uses tracker muons.
    * Probe numerator: Passes medium Muon HIP-safe ID and `d_xy < 0.045` and `d_z < 0.2`
    * pt x abs(eta) bins: [10., 15., 20., 25., 30., 40., 50., 60., 80., 100., 200., 1000.] x [0, 0.9, 1.2, 2.1, 2.4]
    * Data/MC ratio available as `m_id_ratio`
    * Workspace variables to set: `m_pt` and `m_eta`

 - `m_iso_data` and `m_iso_mc`: *double Voigtian* signal pdf, *Exponential* background pdf
    * Probe denominator: numerator of the ID measurement above
    * Probe numerator: Passes `I_rel < 0.15`, where `I_rel` is the delta-beta corrected PF isolation with cone size 0.4
    * pt x abs(eta) bins: [20., 25., 30., 40., 50., 60., 80., 100., 200., 1000.] x [0, 0.9, 1.2, 2.1, 2.4]
    * Data/MC ratio available as `m_iso_ratio`
    * Workspace variables to set: `m_pt` and `m_eta`

 - For convenience, product of ID and iso factors available as `m_idiso_[data,mc,ratio]`

 - `m_trg_data` and `m_trgOR_data`: *double Voigtian* signal pdf, *Exponential* background pdf
    * Probe denominator: numerator of the Iso measurement above
    * Probe numerator: For `m_trg_data`: fires the `HLT_IsoMu22` path and matches the final HLT filter object within `DR < 0.5`. For `m_trgOR_data` use the OR of the `HLT_IsoMu22` and `HLT_IsoTkMu22` paths
    * pt x abs(eta) bins: [20., 21., 22., 23., 24., 25., 30., 40., 50., 60., 80., 100., 200., 1000.] x [0, 0.9, 1.2, 2.1, 2.4]
    * Workspace variables to set: `m_pt` and `m_eta`

 - `m_trgMT_data` and `m_trgMTL1_data`: *double Voigtian* signal pdf, *Exponential* background pdf
    * Probe denominator: numerator of the Iso measurement above. For `m_trgMT_data` also require some other well separate object in the event fired the L1 tau part.
    * Probe numerator: For both triggers require that the muon part fired by matching to the final muon filter HLT object within `DR < 0.5`.
    * pt x abs(eta) bins: [17., 18., 19., 20., 21., 22., 25., 30., 40., 50., 60., 80., 100., 200., 1000.] x [0, 0.9, 1.2, 2.1]
    * Workspace variables to set: `m_pt` and `m_eta`

Additional isolation and trigger efficiencies have been measured with isolation definitions in the numerator and denominator probe selections respectively: `I_rel = [0.15, 0.25]` and `I_rel = [0.25, 0.50]`. These are available via the following functions:

 - `m_iso_binned_data` and `m_iso_binned_mc`: *double Voigtian* signal pdf, *Exponential* background pdf
    * pt x abs(eta) bins: [20., 25., 30., 40., 50., 60., 80., 100., 200., 1000.] x [0, 0.9, 1.2, 2.1, 2.4]
    * Data/MC ratio available as `m_iso_binned_ratio`
    * Workspace variables to set: `m_pt`, `m_eta` and `m_iso`

 - `m_trg_binned_data` and `m_trgOR_binned_data`: *double Voigtian* signal pdf, *Exponential* background pdf
    * pt x abs(eta) bins: [20., 21., 22., 23., 24., 25., 30., 40., 50., 60., 80., 100., 200., 1000.] x [0, 0.9, 1.2, 2.1, 2.4] for the nominal isolation, and [20., 21., 22., 23., 24., 25., 30., 40., 50., 60., 80., 100., 1000.] x [0, 2.4] for the additional isolation bins due to the lower number of events.
    * Workspace variables to set: `m_pt`, `m_eta` and `m_iso`

### Electrons

 **Note that all electron measurements have been made using the electron supercluster eta - you should use this as the `e_eta` input**

 - `e_id_data` and `e_id_mc`: *double Voigtian* signal pdf, *RooCMSShape* background pdf
    * Probe denominator: all electrons `slimmedElectrons` collection, `pt > 10` and `abs(eta) < 2.5`
    * Probe numerator: Passes MVA non-triggering ID and `d_xy < 0.045` and `d_z < 0.2`
    * pt x abs(eta) bins: [10., 20., 25., 30., 40., 50., 100., 200., 1000.] x [0, 1.0, 1.4442, 1.56, 2.1, 2.5]
    * Data/MC ratio available as `e_id_ratio`
    * Workspace variables to set: `e_pt` and `e_eta`

 - `e_iso_data` and `e_iso_mc`: *double Voigtian* signal pdf, *Exponential* background pdf
    * Probe denominator: numerator of the ID measurement above
    * Probe numerator: Passes `I_rel < 0.10`, where `I_rel` is the delta-beta corrected PF isolation with cone size 0.3
    * pt x abs(eta) bins: [10., 20., 25., 30., 40., 50., 100., 200., 1000.] x [0, 1.0, 1.4442, 1.56, 2.1, 2.5]
    * Data/MC ratio available as `e_iso_ratio`
    * Workspace variables to set: `e_pt` and `e_eta`

 - For convenience, product of ID and iso factors available as `e_idiso_[data,mc,ratio]`

 - `e_trg_data`: *double Voigtian* signal pdf, *Exponential* background pdf
    * Probe denominator: numerator of the Iso measurement above
    * Probe numerator: Fires the `HLT_Ele25_eta2p1_WPTight_Gsf` path and matches the final HLT filter object within `DR < 0.5`.
    * pt x abs(eta) bins: [10., 20., 22., 24., 26., 28., 30., 40., 50., 100., 200., 1000.] x [0, 1.0, 1.4442, 1.56, 2.1, 2.5]
    * Workspace variables to set: `e_pt` and `e_eta`

Additional isolation and trigger efficiencies have been measured with isolation definitions in the numerator and denominator probe selections respectively: `I_rel = [0.10, 0.20]` and `I_rel = [0.20, 0.50]`. These are available via the following functions:

 - `e_iso_binned_data` and `e_iso_binned_mc`: *double Voigtian* signal pdf, *Exponential* background pdf
    * pt x abs(eta) bins: [10., 20., 25., 30., 40., 50., 100., 200., 1000.] x [0, 1.0, 1.4442, 1.56, 2.1, 2.5]
    * Data/MC ratio available as `e_iso_binned_ratio`
    * Workspace variables to set: `e_pt`, `e_eta` and `e_iso`

 - `e_trg_binned_data`: *double Voigtian* signal pdf, *Exponential* background pdf
    * pt x abs(eta) bins: [10., 20., 22., 24., 26., 28., 30., 40., 50., 100., 200., 1000.] x [0, 1.0, 1.4442, 1.56, 2.1, 2.5] for the nominal isolation, and [10., 20., 22., 24., 26., 28., 30., 40., 50., 100. 1000.] x [0, 2.5] for the additional isolation bins due to the lower number of events.
    * Workspace variables to set: `e_pt`, `e_eta` and `e_iso`

### Taus
Scale factors are defined as a function of `t_pt`, `t_eta`, and `t_dm` (the integer decay mode of the tau). Currently measurements are made inclusively in pT and eta for each decay mode. However, a minimum pT cut is applied to mirror the offline selection used in the HTT analyses. The following functions are available:

 - `t_iso_mva_m_pt30_sf`: medium MVA isolation working point, tau pT > 30 GeV and abs(eta) < 2.3. Intended for use in the e-tau and mu-tau channels of the MSSM analysis. Workspace variables to set: `t_pt`, `t_eta`, and `t_dm`.
 - `t_iso_mva_t_pt40_eta2p1_sf`: tight MVA isolation working point, tau pT > 40 GeV and abs(eta) < 2.1. Intended for use in the tau-tau channel of the MSSM analysis. Workspace variables to set: `t_pt`, `t_eta`, and `t_dm`.

## Usage
The data and MC efficiencies calculated in the fits are currently stored in TH2D histograms. To minimize the amount of extra work needed to extract these numbers, the TH2Ds have been wrapped in RooFit objects and stored inside a workspace, named `scalefactors_2016_vX.root`. Example usage in C++ and python below:

**C++:**
```cpp
#include "RooWorkspace.h"
#include "RooRealVar.h"

TFile f("scalefactors_2016_v5.root");
RooWorkspace *w = (RooWorkspace*)f.Get("w");
f.Close();

// In the event loop:
w->var("m_pt")->setVal(muon.pt());
w->var("m_eta")->setVal(muon.eta());
double muon_id_scalefactor = w->function("m_id_ratio")->getVal();
double muon_iso_scalefactor = w->function("m_iso_ratio")->getVal();
double muon_trg_efficiency = w->function("m_trg_data")->getVal();

// Alternatively (and slightly faster):
// Create a RooFit function object taking the m_pt, m_eta and m_iso values as arguments
#include "RooFunctor.h"
RooFunctor* m_trg_data_func = w->function("m_trg_binned_data")->functor(w->argSet("m_pt,m_eta,m_iso"))
// In the event loop need to pass an array of the argument:
auto args = std::vector<double>{muon.pt(), muon.eta(), muon.pf04Iso()};
double muon_trg_eff = m_trg_data_func->eval(args.data());
```

**Python:**
```py
import ROOT
from array import array

f = ROOT.TFile("scalefactors_2016_v5.root")
w = f.Get("w")
f.Close()

# In the event loop:
w.var("m_pt").setVal(muon.pt())
w.var("m_eta").setVal(muon.eta())
muon_id_scalefactor = w.function("m_id_ratio").getVal()
muon_iso_scalefactor = w.function("m_iso_ratio").getVal()
muon_trg_efficiency = w.function("m_trg_data").getVal()

# Alternatively (and slightly faster):
# Create a RooFit function object taking the m_pt, m_eta and m_iso values as arguments
m_trg_data_func = w.function("m_trg_binned_data").functor(ROOT.RooArgList(w.argSet("m_pt,m_eta,m_iso")))
# In the event loop need to pass an array of the argument:
muon_trg_eff = m_trg_data_func.eval(array('d', [muon.pt(), muon.eta(), muon.pf04Iso()]))
```

Note that despite the efficiencies currently being measured in bins of absolute eta the signed eta value should still be used here as the argument to `setVal`. The conversion to the absolute value will be performed internally within the workspace. In this way it will be easy to switch to scale factors binned in signed eta in the future. There is also no need to check for pT or eta values outside the bounds of the measurement - the supplied values of `m_pt` and `m_eta` will be adjusted to the bounds of the TH2Ds automatically.

## Other factors
Corrections from other sources are also added to the workspace:

### Electron/Muon tag and probe efficiencies from the DESY group
The [LeptonEfficiencies](https://github.com/CMS-HTT/LeptonEfficiencies) repository is a git submodule located in `inputs/LeptonEfficiencies`. The `makeCorrectionsWorkspace.py` script will first convert the TGraphAsymmErrors objects containing the efficiencies into TH2Ds binned in pT and eta before wrapping these in RooFit functions. The table below lists the available function names:

|           Function name           | Input variables |                    Created from input                    |
|-----------------------------------|-----------------|----------------------------------------------------------|
| m_idiso0p15_desy_[mc,data,ratio]  | m_pt,m_eta      | Muon/Run2016BCD/Muon_IdIso0p15_eff.root                  |
| m_idiso0p20_desy_[mc,data,ratio]  | m_pt,m_eta      | Muon/Run2016BCD/Muon_IdIso0p20_eff.root                  |
| m_idiso0p20_desy_data             | m_pt,m_eta      | Muon/Run2016BCD/Muon_IdIso0p20_eff.root                  |
| m_trgIsoMu22_desy_data            | m_pt,m_eta      | Muon/Run2016BCD/Muon_IsoMu22_eff_fineBinning.root                    |
| m_trgIsoMu22orTkIsoMu22_desy_data | m_pt,m_eta      | Muon/Run2016BCD/Muon_IsoMu22_OR_TkIsoMu22_eff_fineBinning.root       |
| m_trgMu8leg_desy_data             | m_pt,m_eta      | Muon/Run2016BCD/Muon_Mu8leg_eff.root                     |
| m_trgMu23leg_desy_data            | m_pt,m_eta      | Muon/Run2016BCD/Muon_Mu23leg_eff.root                    |
| e_idiso0p10_desy_[mc,data,ratio]  | e_pt,e_eta      | Electron/Run2016BCD/Electron_IdIso0p10_eff.root          |
| e_idiso0p15_desy_[mc,data,ratio]  | e_pt,e_eta      | Electron/Run2016BCD/Electron_IdIso0p15_eff.root          |
| e_trgEle25eta2p1WPTight_desy_data | e_pt,e_eta      | Electron/Run2016BCD/Electron_Ele25eta2p1WPTight_eff_fineBinning.root |
| e_trgEle12leg_desy_data           | e_pt,e_eta      | Electron/Run2016BCD/Electron_Ele12leg_eff.root           |
| e_trgEle23leg_desy_data           | e_pt,e_eta      | Electron/Run2016BCD/Electron_Ele23leg_eff.root           |

### Muon and EGamma POG tracking efficiency scale factors

The eta-dependent scale factor histogram from [here](https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2#Tracking_efficiency_provided_by) has been added as the function `m_trk_ratio`. Similarly the pt and eta-dependent scale factors from [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaIDRecipesRun2#Electron_efficiencies_and_scale) has been added as the function `e_trk_ratio`.

### Tau trigger turn-on curves

The [triggerSF](https://github.com/rmanzoni/triggerSF) repository is a git submodule located in `inputs/triggerSF`. The efficiencies are given as functions of tau pT using a convolution of a CrystalBall resolution and a step function. Since such a function does not exist natively in ROOT, the function provided [here](https://github.com/rmanzoni/triggertools/blob/master/objects/FitFunctions.py#L120) has been converted into a RooFit function class and saved in this repository (`CrystalBallEfficiency.h` and `CrystalBallEfficiency.cxx`). The `makeCorrectionsWorkspace.py` script will build a CrystalBallEfficiency object for each parameter set in the `real_taus_cumulative.json` and `same_sign_cumulative.json` input files. The function objects are named like `t_trg[WP_LABEL]_data` and `t_trg[WP_LABEL]SS_data` respectively.

**IMPORTANT**: If desired you can add the code for the CrystalBallEfficiency class to your framework and compile a ROOT dictionary from it. However this is not required for reading from the workspace as RooFit has a mechanism to embed the class code in the workspace itself and generate the dictionary on the fly. When the workspace is first opened a message like

    [#1] INFO:ObjectHandling -- RooWorkspace::CodeRepo::compileClasses() creating code export directory .wscode.963a5b90-58a3-31e6-9717-bfb44a46514d.w to extract coded embedded in workspace
    [#1] INFO:ObjectHandling -- RooWorkspace::CodeRepo::compileClasses() Extracting declaration code of class CrystalBallEfficiency, file .wscode.963a5b90-58a3-31e6-9717-bfb44a46514d.w/CrystalBallEfficiency.h
    [#1] INFO:ObjectHandling -- RooWorkspace::CodeRepo::compileClasses() Extracting implementation code of class CrystalBallEfficiency, file .wscode.963a5b90-58a3-31e6-9717-bfb44a46514d.w/CrystalBallEfficiency.cxx
    [#1] INFO:ObjectHandling -- RooWorkspace::CodeRepo::compileClasses() Compiling code unit CrystalBallEfficiency to define class CrystalBallEfficiency

will be produced. This step does incur a few seconds delay, though this should only happen the first time a workspace is opened. If a dictionary for the class is already known to ROOT then this step will be skipped automatically.

**NB**: It appears in some older versions of CMSSW (e.g. `7_1_5`), the RooFit headers are not included in the default ROOT search path. If you have problems with the CrystalBallEfficiency class not compiling automatically then do this before accessing the workspace:

    gSystem->AddIncludePath("-I$ROOFITSYS/include")

### Z pT weights

Available via the function `zpt_weight` which takes the generator Z boson mass `z_gen_mass` and pT `z_gen_pt` as input.
