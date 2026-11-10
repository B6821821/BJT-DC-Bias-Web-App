# BJT DC Bias Web App

Flask web application for the DC operating point of a BJT Common-Emitter
amplifier with **voltage-divider bias** (Forward-Active approximation).

ENG29 2121 — Lab 02

## Requirements

- Python 3.13 or newer
- pip

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```powershell
python -m flask --app app run --debug
```

Open <http://127.0.0.1:5000/> in a browser.

> The app must be started through the Flask server. Opening
> `templates/index.html` directly with `file://` does not work, because the
> calculation runs in the Python backend.

## Test

```powershell
python -m unittest discover -s tests -v
```

## Project layout

```
.
├── app.py              # Flask application and HTTP routes
├── dc_bias.py          # DC bias engineering calculations
├── templates/
│   └── index.html      # input form + results (Jinja)
├── static/
│   └── style.css       # layout and presentation
├── tests/
│   ├── test_dc_bias.py # unit tests for the engineering logic
│   └── test_web.py     # Flask HTTP route tests
├── requirements.txt
└── docs/
```

## Model

Forward-Active approximation with constant beta and VBE:

```
VTH = VCC * R2 / (R1 + R2)
RTH = R1 * R2 / (R1 + R2)
IB  = (VTH - VBE) / (RTH + (beta + 1) * RE)
IC  = beta * IB
IE  = (beta + 1) * IB
VE  = IE * RE
VB  = VE + VBE
VC  = VCC - IC * RC
VCE = VC - VE
```

The model is only valid in the forward-active region. Results outside that
region (cutoff or saturation) must be reported with a warning.

## Reference values

For `VCC=12 V, R1=100 kOhm, R2=22 kOhm, RC=2.2 kOhm, RE=1 kOhm, beta=100, VBE=0.70 V`:

| Quantity | Value |
| --- | --- |
| VTH | 2.1639 V |
| RTH | 18.0328 kOhm |
| IB | 12.299 uA |
| IC | 1.2299 mA |
| IE | 1.2422 mA |
| VB | 1.9422 V |
| VE | 1.2422 V |
| VC | 9.2943 V |
| VCE | 8.0522 V |
