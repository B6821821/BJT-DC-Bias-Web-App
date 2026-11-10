"""Flask application for the BJT DC Bias calculator.

Routes:
    GET  /        — show the input form (default = reference values)
    POST /calculate — read form, call dc_bias.calculate_dc_bias, render result
"""

from flask import Flask, render_template, request

from dc_bias import calculate_dc_bias, parse_number

app = Flask(__name__)

FIELDS = ("vcc", "r1", "r2", "rc", "re", "beta", "vbe")

LABELS = {
    "vcc": "VCC",
    "r1": "R1",
    "r2": "R2",
    "rc": "RC",
    "re": "RE",
    "beta": "β",
    "vbe": "VBE",
}

DEFAULTS = {
    "vcc": "12",
    "r1": "100",
    "r2": "22",
    "rc": "2.2",
    "re": "1",
    "beta": "100",
    "vbe": "0.70",
}


@app.get("/")
def index():
    return render_template(
        "index.html",
        form=DEFAULTS,
        result=None,
        error=None,
    )


@app.post("/calculate")
def calculate():
    form = {key: (request.form.get(key) or "").strip() for key in FIELDS}
    try:
        values = {
            key: parse_number(form[key], LABELS[key]) for key in FIELDS
        }
        result = calculate_dc_bias(**values)
        region_class = "region-" + result["region"].lower().replace(" ", "-")
    except ValueError as exc:
        return (
            render_template(
                "index.html",
                form=form,
                result=None,
                error=str(exc),
            ),
            400,
        )
    return render_template(
        "index.html",
        form=form,
        result=result,
        region_class=region_class,
        error=None,
    )
