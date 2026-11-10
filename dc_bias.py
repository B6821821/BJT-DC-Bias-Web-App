"""DC bias calculations for BJT Common-Emitter voltage-divider bias.

Pure engineering module — does not import Flask.  All resistor inputs are in
kΩ and are converted to Ω inside this module.  Returns a plain ``dict`` so
the values are easy to test and easy to render in a Jinja template.
"""

KILO = 1000.0          # Ω per kΩ
VCE_SAT_MAX = 0.3      # V — upper bound of VCE treated as "saturation"


def parse_number(raw, label):
    """Convert a form string to a finite float.

    Raises ValueError naming the field when the input is missing, not a
    number, or not finite (nan / inf).
    """
    if raw is None:
        raise ValueError(f"กรุณากรอก {label}")
    text = str(raw).strip()
    if text == "":
        raise ValueError(f"กรุณากรอก {label}")
    try:
        value = float(text)
    except (TypeError, ValueError):
        raise ValueError(f"กรุณากรอก {label} เป็นตัวเลข")
    if value != value or value in (float("inf"), float("-inf")):  # nan / inf
        raise ValueError(f"กรุณากรอก {label} เป็นตัวเลขที่ถูกต้อง")
    return value


def calculate_dc_bias(vcc, r1, r2, rc, re, beta, vbe):
    """Forward-Active DC bias for a voltage-divider biased Common-Emitter.

    Parameters are in mixed SI-friendly units:
        vcc  [V], r1..re [kΩ], beta [-], vbe [V]

    Returns a dict with SI floats (V, A) plus ``rth_kohm`` in kΩ:

        vth, rth_kohm, ib, ic, ie, vb, ve, vc, vce, region, warnings

    Region decision:
        VTH <= VBE           → Cutoff        (IB = IC = IE = 0)
        otherwise VCE <= 0.3 → Saturation    (Forward-Active numbers + warning)
        otherwise            → Forward Active
    """
    # ---- validation (resistor values are in kΩ) ---------------------------
    if vcc <= 0:
        raise ValueError("VCC ต้องมากกว่า 0 V")
    if r1 <= 0:
        raise ValueError("R1 ต้องมากกว่า 0 kΩ")
    if r2 <= 0:
        raise ValueError("R2 ต้องมากกว่า 0 kΩ")
    if rc <= 0:
        raise ValueError("RC ต้องมากกว่า 0 kΩ")
    if re <= 0:
        raise ValueError("RE ต้องมากกว่า 0 kΩ")
    if beta <= 0:
        raise ValueError("β ต้องมากกว่า 0")
    if vbe <= 0 or vbe >= vcc:
        raise ValueError("VBE ต้องมากกว่า 0 V และน้อยกว่า VCC")

    # ---- Thevenin equivalent at the base ----------------------------------
    vth = vcc * r2 / (r1 + r2)          # [V]
    rth_kohm = r1 * r2 / (r1 + r2)      # [kΩ]
    rth = rth_kohm * KILO               # [Ω]
    re_ohm = re * KILO                  # [Ω]
    rc_ohm = rc * KILO                  # [Ω]

    warnings = []

    # ---- Cutoff: Thevenin voltage cannot even reach VBE -------------------
    if vth <= vbe:
        region = "Cutoff"
        ib = 0.0
        ic = 0.0
        ie = 0.0
        ve = 0.0
        vb = vth
        vc = vcc
        vce = vc - ve
        warnings.append(
            f"VTH ({vth:.4f} V) ≤ VBE ({vbe:.2f} V) → ไม่มีกระแสเบส "
            f"ไบแอสนี้อยู่ในช่วง Cutoff"
        )
        return {
            "vth": vth,
            "rth_kohm": rth_kohm,
            "ib": ib,
            "ic": ic,
            "ie": ie,
            "vb": vb,
            "ve": ve,
            "vc": vc,
            "vce": vce,
            "region": region,
            "warnings": warnings,
        }

    # ---- Forward-Active ----------------------------------------------------
    ib = (vth - vbe) / (rth + (beta + 1) * re_ohm)   # [A]
    ic = beta * ib                                     # [A]
    ie = (beta + 1) * ib                               # [A]
    ve = ie * re_ohm                                   # [V]
    vb = ve + vbe                                      # [V]
    vc = vcc - ic * rc_ohm                             # [V]
    vce = vc - ve                                      # [V]

    region = "Forward Active"

    if vce <= VCE_SAT_MAX:
        region = "Saturation"
        warnings.append(
            f"VCE ({vce:.4f} V) ≤ 0.3 V → อาจอยู่ในช่วง Saturation; "
            f"ค่าที่แสดงคำนวณจากสมการ Forward-Active ซึ่งไม่ใช้บังคับในโหมดนี้"
        )

    return {
        "vth": vth,
        "rth_kohm": rth_kohm,
        "ib": ib,
        "ic": ic,
        "ie": ie,
        "vb": vb,
        "ve": ve,
        "vc": vc,
        "vce": vce,
        "region": region,
        "warnings": warnings,
    }
