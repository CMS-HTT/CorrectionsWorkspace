# Correction factors

## Producing the workspace
Clone this repository and initialise the other repositories which are handled as git submodules:

    git clone https://github.com/CMS-HTT/CorrectionsWorkspace.git
    cd CorrectionsWorkspace
    git submodule update --init

The workspace is produced my running the following script:

    python makeCorrectionsWorkspace.py

The contents of the output can be inspected with:

    root -l htt_scalefactors_v2.root
    w->Print()
    # See more detail on the evaluation of a particular object:
    w->function("m_id_ratio")->Print("tree")

## Available corrections

Each name here corresponds to a RooFit function object in the workspace. See below for usage.

 - `m_id_data` and `m_id_mc`: *double Voigtian* signal pdf, *RooCMSShape* background pdf
    * Probe denominator: tracker muons in `slimmedMuons` collection, `pt > 20` and `abs(eta) < 2.4`
    * Probe numerator: Passes medium Muon HIP-safe ID and `d_xy < 0.045` and `d_z < 0.2`
    * pt x abs(eta) bins: [20., 25., 30., 40., 50., 60., 80., 100., 200.] x [0, 0.9, 1.2, 2.1, 2.4]
    * Data/MC ratio available as `m_id_ratio`
    * Workspace variables to set: `m_pt` and `m_eta`

 - `m_iso_data` and `m_iso_mc`: *double Voigtian* signal pdf, *Exponential* background pdf
    * Probe denominator: numerator of the ID measurement above
    * Probe numerator: Passes `I_rel < 0.15`, where `I_rel` is the delta-beta corrected PF isolation with cone size 0.4
    * pt x abs(eta) bins: [20., 25., 30., 40., 50., 60., 80., 100., 200.] x [0, 0.9, 1.2, 2.1, 2.4]
    * Data/MC ratio available as `m_iso_ratio`
    * Workspace variables to set: `m_pt` and `m_eta`

 - `m_trg_data`: *double Voigtian* signal pdf, *Exponential* background pdf
    * Probe denominator: numerator of the Iso measurement above
    * Probe numerator: Fires the `HLT_IsoMu22` path and matches the final HLT filter object within `DR < 0.5`
    * pt x abs(eta) bins: [20., 21., 22., 23., 24., 25., 30., 40., 50., 60., 80., 100., 200.] x [0, 0.9, 1.2, 2.1, 2.4]
    * Data/MC ratio available as `m_iso_ratio`
    * Workspace variables to set: `m_pt` and `m_eta`

Additional isolation and trigger efficiencies have been measured with isolation definitions in the numerator and denominator probe selections respectively: `I_rel = [0.15, 0.25]` and `I_rel = [0.25, 0.50]`. These are available via the following functions:

 - `m_iso_binned_data` and `m_iso_binned_mc`: *double Voigtian* signal pdf, *Exponential* background pdf
    * pt x abs(eta) bins: [20., 25., 30., 40., 50., 60., 80., 100., 200.] x [0, 0.9, 1.2, 2.1, 2.4]
    * Data/MC ratio available as `m_iso_binned_ratio`
    * Workspace variables to set: `m_pt`, `m_eta` and `m_iso`

 - `m_trg_binned_data`: *double Voigtian* signal pdf, *Exponential* background pdf
    * pt x abs(eta) bins: [20., 21., 22., 23., 24., 25., 30., 40., 50., 60., 80., 100., 200.] x [0, 0.9, 1.2, 2.1, 2.4] for the nominal isolation, and [20., 21., 22., 23., 24., 25., 30., 40., 50., 60., 80., 100., 200.] x [0, 2.4] for the additional isolation bins due to the lower number of events.
    * Workspace variables to set: `m_pt`, `m_eta` and `m_iso`

## Usage
The data and MC efficiencies calculated in the fits are currently stored in TH2D histograms. To minimize the amount of extra work needed to extract these numbers, the TH2Ds have been wrapped in RooFit objects and stored inside a workspace, named `scalefactors_2016_vX.root`. Example usage in C++ and python below:

**C++:**
```cpp
#include "RooWorkspace.h"

TFile f("scalefactors_2016_v1.root");
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

f = ROOT.TFile("scalefactors_2016_v1.root")
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

|           Function name           |                    Created from input                    |
|-----------------------------------|----------------------------------------------------------|
| m_idiso0p15_desy_[mc,data,ratio]  | Muon/Run2016BCD/Muon_IdIso0p15_eff.root                  |
| m_idiso0p20_desy_[mc,data,ratio]  | Muon/Run2016BCD/Muon_IdIso0p20_eff.root                  |
| m_idiso0p20_desy_data             | Muon/Run2016BCD/Muon_IdIso0p20_eff.root                  |
| m_trgIsoMu22_desy_data            | Muon/Run2016BCD/Muon_IsoMu22_eff.root                    |
| m_trgIsoMu22orTkIsoMu22_desy_data | Muon/Run2016BCD/Muon_IsoMu22_OR_TkIsoMu22_eff.root       |
| e_idiso0p10_desy_[mc,data,ratio]  | Electron/Run2016BCD/Electron_IdIso0p10_eff.root          |
| e_idiso0p15_desy_[mc,data,ratio]  | Electron/Run2016BCD/Electron_IdIso0p15_eff.root          |
| e_trgEle25eta2p1WPTight_desy_data | Electron/Run2016BCD/Electron_Ele25eta2p1WPTight_eff.root |

### Muon POG tracking efficiency scale factor

The eta-dependent scale factor histogram from [here](https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2#Tracking_efficiency_provided_by) has been added as the function `m_trk_ratio`.

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

