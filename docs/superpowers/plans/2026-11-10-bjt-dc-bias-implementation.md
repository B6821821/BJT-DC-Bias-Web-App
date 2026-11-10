# BJT DC Bias Web App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-page Flask web app that computes BJT Common-Emitter voltage-divider DC bias (VB, VE, VC, VCE, IC plus IB/IE) with kΩ resistor inputs, input validation, forward-active warnings, unit tests, Flask client tests, and docs matching the Lab 02 repo structure.

**Architecture:** Pure calculation module `dc_bias.py` (no Flask import) → Flask routes in `app.py` → Jinja template `templates/index.html` + `static/style.css` → `tests/test_dc_bias.py` and `tests/test_web.py` → docs (`AGENTS.md`, `docs/design-note.md`, `docs/validation.md`, `docs/reflection.md`, `docs/test-log.txt`).

**Tech Stack:** Python 3.13.17, Flask 3.1.3 (venv), unittest (stdlib), Jinja2, HTML/CSS only — no JavaScript.

**Spec:** `docs/superpowers/specs/2026-11-10-bjt-dc-bias-design.md` (approved; resistor inputs in kΩ, single `dict`-returning function).

## Global Constraints

- Resistor inputs are kΩ (backend multiplies by 1000); labels show `(kΩ)`.
- `calculate_dc_bias(...) -> dict` is a single pure function, no dataclass/class.
- No JavaScript; page must work via Flask server at `http://127.0.0.1:5000/`, not `file://`.
- Validation: R≤0, β≤0, VCC≤0, missing/non-numeric → readable Thai error, page must not crash, HTTP 400, keep entered values.
- Warning: VTH ≤ VBE → Cutoff; VCE ≤ 0.3 V → Saturation.
- Tests: ≥3 unit tests + ≥1 Flask test-client test (plan delivers 11).
- commit via GitHub Desktop; do not commit `.venv/`, `__pycache__/`, `.env`.
- Reference values: VCC=12, R1=100k, R2=22k, RC=2.2k, RE=1k, β=100, VBE=0.70 → VB=1.9422 V, VE=1.2422 V, VC=9.2943 V, VCE=8.0522 V, IC=1.2299 mA, IB=12.299 µA.

## Review Focus (input classes not directly exercised by named tasks)

1. Empty/missing form field → `ValueError` with field name; page stays alive.
2. Non-numeric text (e.g. `abc`) → `ValueError` from `parse_number`, HTTP 400, value kept in form.
3. Negative R/β/VCC → rejection message names the offending field.
4. `nan` / `inf` after float() → rejected as non-finite.
5. VTH exactly equal VBE → Cutoff branch (boundary condition).

---

## Tasks

### Task 1: dc_bias.py — pure calculation module

**Files:**
- Create: `dc_bias.py`
- Create: `tests/test_dc_bias.py`

**Interfaces:**
- Consumes: nothing (stdlib only)
- Produces: `KILO = 1000.0`, `VCE_SAT_MAX = 0.3`, `parse_number(raw, label) -> float`, `calculate_dc_bias(vcc, r1, r2, rc, re, beta, vbe) -> dict` with keys `vth, rth_kohm, ib, ic, ie, vb, ve, vc, vce, region, warnings`.

- [ ] **Step 1: Write failing test** `tests/test_dc_bias.py::test_reference_values_forward_active` asserting the §5.9 reference values match `calculate_dc_bias(12, 100, 22, 2.2, 1, 100, 0.70)` to 4 decimals and `region == "Forward Active"`, `warnings == []`.

- [ ] **Step 2: Run `python -m unittest tests.test_dc_bias -v`** → ImportError / AttributeError (module not found).

- [ ] **Step 3: Implement `dc_bias.py`** with `parse_number` (strip, float, reject non-finite → ValueError naming field) and `calculate_dc_bias` (validation order: VCC, R1, R2, RC, RE, β, VBE; Thevenin; Cutoff if VTH ≤ VBE; Forward-Active otherwise; Saturation warning if VCE ≤ 0.3; return SI floats).

- [ ] **Step 4: Run `python -m unittest tests.test_dc_bias -v`** → all dc_bias tests pass.

- [ ] **Step 5: Commit** `dc_bias.py`, `tests/test_dc_bias.py`.

---

### Task 2: Flask app, template, and stylesheet

**Files:**
- Create: `app.py`
- Create: `templates/index.html`
- Create: `static/style.css`

**Interfaces:**
- Consumes: `calculate_dc_bias`, `parse_number` from `dc_bias.py`.
- Produces: Flask routes `GET /` (empty/default form) and `POST /calculate` (parse form, call calculation, render same template; ValueError → HTTP 400 with error kept), template receives `form`, `result`, `error`.

- [ ] **Step 1: Implement `app.py`** — `FIELDS = ("vcc","r1","r2","rc","re","beta","vbe")`, defaults matching reference values, `POST /calculate` parses each field with `parse_number`, catches `ValueError` → `render_template(..., error=str(exc))`, 400.

- [ ] **Step 2: Implement `templates/index.html`** — Thai labels, `<input type="text" step="any" inputmode="decimal" required>`, Jinja renders `result` values formatted (V 4dp, mA/µA, kΩ 4dp), region badge, `error` red box, `warnings` yellow box, keeps `form` values.

- [ ] **Step 3: Implement `static/style.css`** — system-ui font, 2-column grid collapsing to 1 column on narrow screens, max-width ~760 px, no animation/CDN.

- [ ] **Step 4: Manual smoke test** — `python -m flask --app app run --debug`, open `http://127.0.0.1:5000/`, submit reference values, confirm `VB 1.9422`, region `Forward Active`, no JS errors.

- [ ] **Step 5: Commit** `app.py`, `templates/index.html`, `static/style.css`.

---

### Task 3: Flask client tests + full test suite

**Files:**
- Create: `tests/test_web.py`
- Modify: `tests/test_dc_bias.py` (add remaining 6 unit tests)

**Interfaces:**
- Consumes: Flask `app` object from `app.py`, `calculate_dc_bias` from `dc_bias.py`.
- Produces: 11 total tests passing via `python -m unittest discover -s tests -v`.

- [ ] **Step 1: Add remaining unit tests** to `tests/test_dc_bias.py` — Thevenin equivalents, Cutoff (VTH ≤ VBE → IC=0, VCE=VCC), Saturation warning (VCE ≤ 0.3 → warnings non-empty), higher β → higher IC, invalid R/β/VCC → ValueError naming field, `parse_number("abc","R1")` → ValueError containing "R1".

- [ ] **Step 2: Write `tests/test_web.py`** — Flask test client: `GET /` → 200 has VCC/R1; `POST` reference values → 200 has `1.9422` and `Forward Active`; `POST re=0` → 400 has `RE`; `POST vcc=abc` → 400 has number-prompt message.

- [ ] **Step 3: Run `python -m unittest discover -s tests -v`** → 11 tests pass.

- [ ] **Step 4: Commit** `tests/test_dc_bias.py`, `tests/test_web.py`.

---

### Task 4: Lab documentation (AGENTS.md + docs)

**Files:**
- Create: `AGENTS.md`
- Create: `docs/design-note.md`
- Create: `docs/validation.md`
- Create: `docs/reflection.md` (draft; student to personalize wording)

**Interfaces:**
- Consumes: none.
- Produces: repo matches Lab handout structure (`AGENTS.md`, `docs/{design-note,validation,reflection}.md`).

- [ ] **Step 1: Write `AGENTS.md`** — coding conventions for this repo (file responsibilities, naming, no JS, Thai labels, kΩ convention).

- [ ] **Step 2: Write `docs/design-note.md`** — one-page design summary (approach A: kΩ, dict function, Cutoff/Saturation rules).

- [ ] **Step 3: Write `docs/validation.md`** — recorded validation results: reference values match, invalid-input behavior, Cutoff/Saturation warnings, test count.

- [ ] **Step 4: Draft `docs/reflection.md`** — outline of what was learned, decisions made, limitations (saturation branch keeps Forward-Active numbers + warning).

- [ ] **Step 5: Commit** `AGENTS.md`, `docs/design-note.md`, `docs/validation.md`, `docs/reflection.md`.

---

### Task 5: Final verification, test log, handoff

**Files:**
- Create: `docs/test-log.txt`

**Interfaces:**
- Consumes: all prior tasks.
- Produces: `docs/test-log.txt` containing `python -m unittest discover -s tests -v` output; working tree clean; remote in sync.

- [ ] **Step 1: Run `python -m unittest discover -s tests -v > docs/test-log.txt 2>&1`** → capture output; confirm 11 pass, 0 fail.

- [ ] **Step 2: Verify working tree** — `git status` clean except intended new files; `.venv/` ignored.

- [ ] **Step 3: Commit** `docs/test-log.txt` and anything remaining.

- [ ] **Handoff:** tell student the repo is ready; they commit/push via GitHub Desktop and send Repository URL + Commit SHA + screenshot + test log to Moodle.
