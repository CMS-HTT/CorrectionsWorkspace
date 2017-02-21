# Correction factors

**UPDATES**:
 - 21/02, htt_scalefactors_sm_moriond_v1.root

## Using the workspace

Example usage in C++ and python:

**C++:**
```cpp
#include "RooWorkspace.h"
#include "RooRealVar.h"

TFile f("htt_scalefactors_sm_moriond_v1.root");
RooWorkspace *w = (RooWorkspace*)f.Get("w");
f.Close();

// In the event loop:
w->var("t_pt")->setVal(tau.pt());
w->var("t_eta")->setVal(tay.eta());
w->var("t_dm")->setVal(tay.decayMode());
double tau_trigger_sf = w->function("t_fake_VLooseIso_et_ratio")->getVal();

// Alternatively (and slightly faster):
// Create a RooFit function object taking the t_pt, t_eta and t_dm values as arguments
#include "RooFunctor.h"
RooFunctor* t_trg_sf_func = w->function("t_fake_VLooseIso_et_ratio")->functor(w->argSet("t_pt,t_eta,t_dm"))
// In the event loop need to pass an array of the argument:
auto args = std::vector<double>{tau.pt(), tau.eta(), tau.decayMode()};
double tau_trigger_sf = t_trg_df_func->eval(args.data());
```

**Python:**
```py
import ROOT
from array import array

f = ROOT.TFile("htt_scalefactors_sm_moriond_v1.root")
w = f.Get("w")
f.Close()

# In the event loop:
w.var("t_pt").setVal(tau.pt())
w.var("t_eta").setVal(tau.eta())
w.var("t_dm").setVal(tau.decayMode())
tau_trigger_sf = w.function("t_fake_VLooseIso_et_ratio").getVal()

# Alternatively (and slightly faster):
# Create a RooFit function object taking the t_pt, t_eta and t_dm values as arguments
t_trg_sf_func = w.function("t_fake_VLooseIso_et_ratio").functor(ROOT.RooArgList(w.argSet("t_pt,t_eta,t_dm")))
# In the event loop need to pass an array of the argument:
tau_trigger_sf = t_trg_sf_func.eval(array('d', [tau.pt(), tau.eta(), tau.decayMode()]))
```

## Producing the workspace
Clone this repository and initialise the other repositories which are handled as git submodules:

    git clone https://github.com/CMS-HTT/CorrectionsWorkspace.git
    cd CorrectionsWorkspace
    git submodule update --init

The workspace is produced by running the following script:

    python python makeCorrectionsWorkspace_minimal_sm.py

The contents of the output can be inspected with:

    root -l htt_scalefactors_sm_moriond_v1.root
    w->Print()
    # See more detail on the evaluation of a particular object:
    w->function("t_genuine_TightIso_tt_ratio")->Print("tree")

## Available corrections

Each name here corresponds to a RooFit function object in the workspace. See below for usage.

### Taus
Scale factors and efficiencies are defined as a function of some or all of: `t_pt`, `t_eta`, and `t_dm` (the integer decay mode of the tau). The tau-tau channel trigger turn-ons are parameterised by crystal ball functions. See the notes below on the technical implementation.
For the e-tau and mu-tau channels the values are read from TGraphs, with linear interpolation used between points.

|                                     Function name                                      | Input variables |                                    Notes                                     |
|----------------------------------------------------------------------------------------|-----------------|------------------------------------------------------------------------------|
| `t_[genuine,fake]_[VLoose,Loose,Medium,Tight,VTight,VVTight]Iso_tt_[mc,data,ratio]`    | t_pt,t_dm       | Tau-tau channel efficiencies. Inclusive in eta, binned in DM for data and MC |
| `t_[genuine,fake]_[No,VLoose,Loose,Medium,Tight,VTight,VVTight]Iso_mt_[mc,data,ratio]` | t_pt,t_eta      | Mu-tau channel efficiencies. Inclusive in DM, binned in eta                  |
| `t_[genuine,fake]_[No,VLoose,Loose,Medium,Tight,VTight,VVTight]Iso_et_[data,ratio]`    | t_pt,t_eta,t_dm | El-tau channel efficiencies for data. Binned in DM and eta.                  |
| `t_[genuine,fake]_[No,VLoose,Loose,Medium,Tight,VTight,VVTight]Iso_et_[mc]`            | t_pt,t_eta      | El-tau channel efficiencies for MC. Inclusive in DM and binned in eta        |



### CrystalBall functions

The efficiencies are given as functions of tau pT using a convolution of a CrystalBall resolution and a step function. Since such a function does not exist natively in ROOT, the function provided [here](https://github.com/rmanzoni/triggertools/blob/master/objects/FitFunctions.py#L120) has been converted into a RooFit function class and saved in this repository (`CrystalBallEfficiency.h` and `CrystalBallEfficiency.cxx`).

**IMPORTANT**: If desired you can add the code for the CrystalBallEfficiency class to your framework and compile a ROOT dictionary from it. However this is not required for reading from the workspace as RooFit has a mechanism to embed the class code in the workspace itself and generate the dictionary on the fly. When the workspace is first opened a message like

    [#1] INFO:ObjectHandling -- RooWorkspace::CodeRepo::compileClasses() creating code export directory .wscode.963a5b90-58a3-31e6-9717-bfb44a46514d.w to extract coded embedded in workspace
    [#1] INFO:ObjectHandling -- RooWorkspace::CodeRepo::compileClasses() Extracting declaration code of class CrystalBallEfficiency, file .wscode.963a5b90-58a3-31e6-9717-bfb44a46514d.w/CrystalBallEfficiency.h
    [#1] INFO:ObjectHandling -- RooWorkspace::CodeRepo::compileClasses() Extracting implementation code of class CrystalBallEfficiency, file .wscode.963a5b90-58a3-31e6-9717-bfb44a46514d.w/CrystalBallEfficiency.cxx
    [#1] INFO:ObjectHandling -- RooWorkspace::CodeRepo::compileClasses() Compiling code unit CrystalBallEfficiency to define class CrystalBallEfficiency

will be produced. This step does incur a few seconds delay, though this should only happen the first time a workspace is opened. If a dictionary for the class is already known to ROOT then this step will be skipped automatically.

**NB**: It appears in some older versions of CMSSW (e.g. `7_1_5`), the RooFit headers are not included in the default ROOT search path. If you have problems with the CrystalBallEfficiency class not compiling automatically then do this before accessing the workspace:

    gSystem->AddIncludePath("-I$ROOFITSYS/include")

