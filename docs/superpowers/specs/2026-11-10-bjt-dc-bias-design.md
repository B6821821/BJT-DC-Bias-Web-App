# Design — BJT DC Bias Web App (ENG29 2121 Lab 02)

วันที่: 2026-11-10
สถานะ: รออนุมัติจากเจ้าของงาน

---

## 1. Intent — ทำไมต้องมีงานนี้

ส่งงาน Lab 02 ของ ENG29 2121: เว็บแอปที่คำนวณ **จุดทำงาน DC (DC operating point)** ของ
BJT ต่อแบบ **Common-Emitter with voltage-divider bias** โดยใช้สมการ Forward-Active
แบบ β คงที่ และ VBE คงที่

คุณค่าที่แท้จริงไม่ใช่ตัวเว็บ แต่คือ **นักศึกษาต้องอธิบายโค้ดของตัวเองได้ตอนตอบคำถามรายบุคคล**
และต้องผ่านเกณฑ์ตรวจรับ A1–A7 ในคาบเดียว ดังนั้นเป้าหมายคือ *เล็ก แต่ครบและอธิบายได้ทุกบรรทัด*
ไม่ใช่ production-grade

---

## 2. Goals / Non-goals / Anti-goals

### Goals

| # | เป้าหมาย |
|---|---|
| G1 | รับค่า `VCC, R1, R2, RC, RE, β, VBE` แล้วคำนวณ `VB, VE, VC, VCE, IC` ด้วย Python จริง |
| G2 | แสดง `IB, IE, VTH, RTH` เพิ่มด้วย (ต้นทุนต่ำ + ได้คะแนนหมวด "สมมติฐานชัดเจน") |
| G3 | ทุกค่าที่แสดงมีหน่วยกำกับชัดเจน (V, mA, µA, kΩ) |
| G4 | input ผิด → ข้อความ error ภาษาไทยที่อ่านรู้เรื่อง หน้าไม่ล้ม และคงค่าที่พิมพ์ไว้ |
| G5 | ผลออกนอก forward-active → แจ้ง Cutoff / Saturation อย่างชัดเจน |
| G6 | มี unit tests ของสมการ ≥ 3 และ Flask test client ≥ 1 |
| G7 | clone จาก GitHub → install → run → test ได้ตาม README (A7) |
| G8 | repo ตรงโครงที่เอกสาร Lab แนะนำ: มี `AGENTS.md` และ `docs/{design-note,validation,reflection}.md` |

### Non-goals (ไม่ทำในรอบนี้)

- AC analysis, gain, Bode plot, transient, signal generator, overlay animation
- SPICE / ngspice integration
- ฐานข้อมูล, ระบบ login, การบันทึกประวัติการคำนวณ
- JavaScript (ไม่ต้องมีแม้แต่บรรทัดเดียว)
- REST API แบบ JSON (รับ/ส่ง HTML form เท่านั้น)

### Anti-goals (ทำแล้วถือว่าล้มเหลว แม้เว็บจะเปิดได้)

| Anti-goal | ทำไม |
|---|---|
| ค่าผลลัพธ์ hardcode ใน HTML | ผิดเงื่อนไข Lab โดยตรง ("ผลต้องมาจาก Python") |
| ต้องเปิดผ่าน `file://` | ผิดเงื่อนไข Lab (ต้องรันผ่าน Flask) |
| commit `.venv/` หรือ `__pycache__/` | ผิดกฎ Lab และ repo บวม |
| ใส่ Flask blueprint / dataclass / class / ORM เพื่อ "ทำให้ดูโปร" | อธิบายตอนสอบไม่ทัน และเกินเวลาคาบ |
| เพิ่มกราฟ/แอนิเมชันเพื่อความสวย | เสี่ยงไม่ทัน และไม่ถูกให้คะแนน |

---

## 3. Constraints (ข้อจำกัดที่ควบคุมการออกแบบ)

| ข้อจำกัด | ผลต่อการออกแบบ |
|---|---|
| เวลาทำงานจริงเหลือคาบเดียว | ไฟล์น้อย บรรทัดน้อย ไม่มี abstraction เกินจำเป็น |
| ต้องอธิบายโค้ดเองได้ | ใช้ชื่อตัวแปรตรงกับสมการในเอกสาร (VTH, RTH, IB, IC, IE) |
| Flask เท่านั้น, ไม่เพิ่ม dependency | ใช้ `render_template`, `request.form` — ไม่มี Flask-WTF |
| Python 3.13, Windows + PowerShell | ใช้ `python -m unittest discover` ไม่ใช้ pytest |
| UI ภาษาไทย, ชื่อตัวแปร/คีย์อังกฤษ | label ไทย + symbol อังกฤษ (เช่น `R1 (kΩ)`) |
| commit ทำผ่าน **GitHub Desktop** (ผู้ใช้เป็นคนกด) | ผมสร้าง/แก้ไฟล์เท่านั้น แล้วให้ผู้ใช้ commit ตามข้อความที่เตรียมไว้ |
| repo ต้องให้อาจารย์ clone ได้ | ต้องเป็น Public หรือเชิญอาจารย์เป็น collaborator (ยังค้างอยู่) |

---

## 4. Approaches ที่พิจารณา

### 4.1 หน่วยของตัวต้านทานในฟอร์ม

| ทาง | ลักษณะ | ข้อดี | ข้อเสีย |
|---|---|---|---|
| **A. กรอกเป็น kΩ ตายตัว** ← **เลือก** | label `R1 (kΩ)` ใส่ `100`, backend × 1000 | ตรงกับค่าตัวอย่างในเอกสาร, พิมพ์น้อย, validation ง่าย | ถ้าผู้ใช้พิมพ์ `100000` ผลจะผิด 1000 เท่า |
| B. กรอกเป็น Ω ล้วน | ใส่ `100000` | ไม่ต้องแปลงหน่วย | พิมพ์เยอะ พลาดเลขศูนย์ง่าย |
| C. dropdown เลือก Ω/kΩ ต่อช่อง | ยืดหยุ่นสุด | ตรงกับทุกกรณี | validation/เทสต์ซับซ้อนขึ้นเท่าตัว เสี่ยงไม่ทัน |

**เหตุผลที่เลือก A:** ค่าตัวอย่างที่อาจารย์ใช้ตรวจคือ `100k, 22k, 2.2k, 1k` — การกรอกเป็น kΩ
ทำให้ผู้ตรวจกรอกตามเอกสารได้ตรง ๆ และลดโอกาสพิมพ์ผิด

### 4.2 โครงสร้างโมดูลคำนวณ

| ทาง | ลักษณะ | ข้อดี | ข้อเสีย |
|---|---|---|---|
| **A. ฟังก์ชันเดียวคืน `dict`** ← **เลือก** | `calculate_dc_bias(...) -> dict` | เข้าใจง่าย อธิบายได้ทุกบรรทัด เทสต์ตรงไปตรงมา ส่งเข้า Jinja ได้เลย | ชื่อคีย์พิมพ์ผิดไม่ error จนกว่าจะรัน |
| B. คืน `@dataclass` | `DcBiasResult` | ชื่อฟิลด์ชัด พิมพ์ผิด error ทันที | เพิ่มแนวคิดที่ต้องอธิบายอีกชั้น |
| C. คลาสเก็บ state | `BiasCalculator` | — | มี state โดยไม่จำเป็น เทสต์ยุ่ง ไม่ช่วยอะไรในขนาดงานนี้ |

**เหตุผลที่เลือก A:** เป้าหมายคือ "จบงาน + อธิบายได้" ไม่ใช่สถาปัตยกรรมระดับ production

---

## 5. Design ที่จะสร้าง

### 5.1 โครงไฟล์

```
BJT DC Bias Web App/
├── app.py                    # Flask routes + text→number parsing
├── dc_bias.py                # สมการ + validation (ไม่รู้จัก Flask)
├── templates/
│   └── index.html            # ฟอร์ม + ผลลัพธ์ (Jinja)
├── static/
│   └── style.css             # layout / presentation
├── tests/
│   ├── test_dc_bias.py       # unit tests ของสมการ
│   └── test_web.py           # Flask test client
├── docs/
│   ├── design-note.md        # สรุปการออกแบบสั้น ๆ (โครงที่อาจารย์กำหนด)
│   ├── validation.md         # บันทึกผลตรวจ A3/A4/A5 + ค่าอ้างอิง
│   ├── reflection.md         # ฉบับร่างให้เจ้าของงานแก้ถ้อยคำ
│   ├── test-log.txt          # output ของ unittest (หลักฐานส่งงาน)
│   ├── checklist.md
│   └── superpowers/specs/2026-11-10-bjt-dc-bias-design.md   ← ไฟล์นี้
├── AGENTS.md                 # กติกาการเขียนโค้ดใน repo (โครงที่อาจารย์กำหนด)
├── requirements.txt
└── README.md
```

ไม่มี `__init__.py` ใน `tests/` (unittest discovery จัดการเอง) และไม่มี package ครอบ

### 5.2 `dc_bias.py` — API

```python
KILO = 1000.0
VCE_SAT_MAX = 0.3      # V — ขอบเขตบนของ VCE ในโหมดอิ่มตัว

def parse_number(raw, label) -> float
def calculate_dc_bias(vcc, r1, r2, rc, re, beta, vbe) -> dict
```

- `parse_number(raw, label)`: ตัดช่องว่าง, แปลงเป็น `float`, ถ้าแปลงไม่ได้หรือเป็น
  `nan/inf` → `raise ValueError(f"กรุณากรอก {label} เป็นตัวเลข")`
- `calculate_dc_bias(...)`: รับ **ตัวเลขล้วน** หน่วย SI ผสมตามธรรมชาติของงานคือ
  `vcc` [V], `r1..re` [**kΩ**], `beta` [-], `vbe` [V] — ชื่อพารามิเตอร์เป็น `r1` ไม่ใช่
  `r1_ohm` เพราะ unit ระบุไว้ที่ docstring และ label แล้ว
- ทั้งสองฟังก์ชัน **ไม่ import Flask** → เทสต์ได้โดยไม่ต้องเปิด HTTP
- ข้อผิดพลาดใช้ `ValueError` ธรรมดา (ไม่สร้าง exception class ใหม่ — ตรงกับแนวทาง A)

**Validation (เรียงตามลำดับที่ตรวจ):**

| เงื่อนไข | ข้อความ (ไทย) |
|---|---|
| `vcc <= 0` | `VCC ต้องมากกว่า 0 V` |
| `r1 <= 0` / `r2 <= 0` / `rc <= 0` / `re <= 0` | `R1 ต้องมากกว่า 0 kΩ` (เปลี่ยนชื่อตามฟิลด์) |
| `beta <= 0` | `β ต้องมากกว่า 0` |
| `vbe <= 0` หรือ `vbe >= vcc` | `VBE ต้องมากกว่า 0 และน้อยกว่า VCC` |
| ไม่ใช่ตัวเลข / nan / inf | `กรุณากรอก <label> เป็นตัวเลข` (มาจาก `parse_number`) |

### 5.3 สมการและลำดับการคำนวณ

```
VTH = VCC · R2 / (R1 + R2)                    [V]
RTH = R1 · R2 / (R1 + R2)                     [kΩ]
IB  = (VTH − VBE) / (RTH·1000 + (β+1)·RE·1000)  [A]
IC  = β · IB                                  [A]
IE  = (β + 1) · IB                            [A]
VE  = IE · RE·1000                            [V]
VB  = VE + VBE                                [V]
VC  = VCC − IC · RC·1000                      [V]
VCE = VC − VE                                 [V]
```

**การตัดสินโหมดการทำงาน (สำคัญ):**

```
ถ้า VTH <= VBE:                          → region = "Cutoff"
     IB = IC = IE = 0
     VE = 0, VB = VTH, VC = VCC, VCE = VCC
     warning: "VTH (… V) ≤ VBE (… V) จึงไม่มีกระแสเบส ไบแอสนี้อยู่ในช่วง Cutoff"

มิฉะนั้น ถ้า VCE <= 0.3:                   → region = "Saturation"
     คงค่าที่คำนวณจากสมการ Forward-Active ไว้ แล้วแนบ warning ว่าใช้ไม่ได้
     warning: "VCE (… V) ≤ 0.3 V จึงอยู่ในช่วง Saturation ค่าที่แสดงมาจากสมการ
               Forward-Active ซึ่งไม่ใช้บังคับในโหมดนี้"

มิฉะนั้น:                                  → region = "Forward Active", warnings = []
```

**เหตุผลที่ทำไม่เหมือนกันสองกรณี:** Cutoff มีคำตอบที่แน่นอนและคำนวณถูกได้ทันที (ทรานซิสเตอร์
ดับ → กระแสเป็นศูนย์) จึงคำนวณให้ถูกจริง ส่วน Saturation ต้องสมมติ `VCE_sat` เพิ่มอีกตัว
ซึ่งอยู่นอกขอบเขต Lab (A5 ต้องการแค่ "แจ้งเตือน") จึงคงตัวเลขเดิมไว้พร้อมคำเตือนชัดเจน
— ระบุเป็น **ข้อจำกัดที่รู้ตัว** ไม่ใช่บั๊ก

### 5.4 `dict` ที่คืนออกมา

| คีย์ | หน่วย | ตัวอย่าง (ค่าอ้างอิง) |
|---|---|---|
| `vth` | V | 2.1639 |
| `rth_kohm` | kΩ | 18.0328 |
| `ib` | A | 1.2299e-05 |
| `ic` | A | 1.2299e-03 |
| `ie` | A | 1.2422e-03 |
| `vb` | V | 1.9422 |
| `ve` | V | 1.2422 |
| `vc` | V | 9.2943 |
| `vce` | V | 8.0522 |
| `region` | str | `"Forward Active"` |
| `warnings` | list[str] | `[]` |

ค่าทั้งหมดเป็น **float หน่วย SI** (V, A) ยกเว้น `rth_kohm` ที่เป็น kΩ ตามชื่อคีย์
— ไม่มีสตริงที่จัดรูปแบบแล้วใน dict นี้ (การจัดรูปแบบเป็นหน้าที่ของ template)

### 5.5 `app.py` — routes

| Route | Method | พฤติกรรม |
|---|---|---|
| `/` | GET | แสดงฟอร์มพร้อมค่าเริ่มต้นตัวอย่าง (12, 100, 22, 2.2, 1, 100, 0.70), `result=None` |
| `/calculate` | POST | อ่าน `request.form`, `parse_number` ทุกช่อง, เรียก `calculate_dc_bias`, render หน้าเดิมพร้อมผล |

```python
FIELDS = ("vcc", "r1", "r2", "rc", "re", "beta", "vbe")

@app.post("/calculate")
def calculate():
    form = {k: request.form.get(k, "").strip() for k in FIELDS}
    try:
        values = {k: parse_number(form[k], LABELS[k]) for k in FIELDS}
        result = calculate_dc_bias(**values)
    except ValueError as exc:
        return render_template("index.html", form=form, result=None, error=str(exc)), 400
    return render_template("index.html", form=form, result=result, error=None)
```

- **ไม่ใช้ JavaScript** — หน้าเดียว, POST แล้ว render ใหม่
- คืน **HTTP 400** เมื่อ input ผิด (ยัง render HTML ปกติ ไม่ใช่ error page ของ Flask)
- คงค่าที่ผู้ใช้พิมพ์ไว้ใน `form` ทุกกรณี (ทั้งสำเร็จและ error)

### 5.6 `templates/index.html` — contract

ตัวแปรที่ template ได้รับ: `form` (dict ของ string ดิบ), `result` (dict หรือ `None`), `error` (str หรือ `None`)

```
┌─ BJT DC Bias Calculator ──────────────────────┐
│ ENG29 2121 · Lab 02 · Voltage-Divider Bias    │
├───────────────────────────────────────────────┤
│ VCC [12] V          β   [100]                 │
│ R1  [100] kΩ        R2  [22]  kΩ              │
│ RC  [2.2] kΩ        RE  [1]   kΩ              │
│ VBE [0.70] V                                  │
│              [ คำนวณ DC Bias ]                │
├───────────────────────────────────────────────┤
│ ⚠ (ถ้ามี error → กล่องแดง)                    │
├───────────────────────────────────────────────┤
│ โหมดการทำงาน:  Forward Active                 │
│ VB  1.9422 V      VE  1.2422 V                │
│ VC  9.2943 V      VCE 8.0522 V                │
│ IC  1.2299 mA     IB  12.30 µA                │
│ IE  1.2422 mA                                 │
│ VTH 2.1639 V      RTH 18.0328 kΩ              │
│ (ถ้ามี warning → กล่องเหลือง)                  │
└───────────────────────────────────────────────┘
```

- จัดรูปแบบใน Jinja: V → ทศนิยม 4 ตำแหน่ง, IC/IE → mA 4 ตำแหน่ง, IB → µA 2 ตำแหน่ง
- `<meta charset="utf-8">`, `<html lang="th">`, `<meta name="viewport" ...>`
- ทุก input มี `<label for>` และ `step="any"` `inputmode="decimal"` `required`
- ปุ่ม submit มี type="submit" ใช้ `url_for('calculate')` เป็น action
- ไม่มี CDN / ฟอนต์ภายนอก (ให้เปิดได้ตอนไม่มีเน็ต)

### 5.7 `static/style.css`

- ตัวอักษร system stack (`system-ui, -apple-system, "Segoe UI", sans-serif`)
- ฟอร์มเป็น grid 2 คอลัมน์ บนจอแคบยุบเป็น 1 คอลัมน์ (`@media`)
- ผลลัพธ์เป็นการ์ด/ตาราง อ่านง่าย, badge สีตามโหมด (เขียว/เหลือง/แดง)
- ความกว้างสูงสุด ~ 760 px, พื้นหลังสว่าง, คอนทราสต์ผ่าน WCAG AA
- **ไม่มี animation** (กันเสียเวลาและไม่ถูกให้คะแนน)

### 5.8 Tests

`tests/test_dc_bias.py` — `unittest`, 7 เทสต์

| เทสต์ | ตรวจอะไร |
|---|---|
| `test_reference_values_forward_active` | ชุดค่าอ้างอิง → VTH/RTH/IB/IC/IE/VB/VE/VC/VCE ตรง 4 ตำแหน่ง, region `"Forward Active"`, `warnings == []` |
| `test_thevenin_equivalents` | VTH = 2.1639 V, RTH = 18.0328 kΩ (ตรวจสูตร divider แยก) |
| `test_cutoff_when_vth_below_vbe` | R1=100k, R2=4.7k → VTH ≤ VBE → region `"Cutoff"`, IC == 0, VCE == VCC |
| `test_saturation_warns` | RC=10k → VCE ≤ 0.3 → region `"Saturation"` และ warnings ไม่ว่าง |
| `test_higher_beta_gives_higher_ic` | β=200 ให้ IC มากกว่า β=100 (sanity ของทิศทาง) |
| `test_invalid_components_rejected` | `re=0`, `beta=0`, `vcc=0` → `ValueError` ที่ข้อความอ้างชื่อฟิลด์ |
| `test_parse_number_rejects_text` | `parse_number("abc", "R1")` → `ValueError` มีคำว่า `R1` |

`tests/test_web.py` — Flask test client, 4 เทสต์

| เทสต์ | ตรวจอะไร |
|---|---|
| `test_index_shows_form` | `GET /` → 200, มี `VCC` และ `R1` |
| `test_calculate_shows_results` | `POST /calculate` ชุดค่าอ้างอิง → 200, มี `1.9422` และ `Forward Active` |
| `test_invalid_input_shows_error` | `re=0` → 400, มี `RE`, และค่าที่กรอกยังอยู่ในหน้า |
| `test_non_numeric_shows_error` | `vcc=abc` → 400, มีข้อความบอกให้กรอกเป็นตัวเลข |

รวม **11 เทสต์** (เกินเกณฑ์ A6 ที่ต้องการ 3 + 1)

### 5.9 ค่าอ้างอิงสำหรับตรวจ (A3)

`VCC=12 V, R1=100 kΩ, R2=22 kΩ, RC=2.2 kΩ, RE=1 kΩ, β=100, VBE=0.70 V`

| ปริมาณ | ค่า |
|---|---|
| VTH | 2.1639 V |
| RTH | 18.0328 kΩ |
| IB | 12.299 µA |
| IC | 1.2299 mA |
| IE | 1.2422 mA |
| VB | 1.9422 V |
| VE | 1.2422 V |
| VC | 9.2943 V |
| VCE | 8.0522 V |

ค่านี้ยืนยันแล้วด้วย smoke test Flask จริง (`HTTP 200`, ผลตรงกับคำนวณมือ)

---

## 6. การตัดสินใจที่ผมเลือกให้ (แก้ได้ถ้าคุณไม่เห็นด้วย)

| เรื่อง | ที่เลือก | เหตุผล |
|---|---|---|
| Route | `POST /calculate` | แยก GET/POST ชัด ตรงกับ A2 |
| หน้า | หน้าเดียว ไม่มี JS | ตามเอกสาร, ลดจุดพัง |
| IB/IE/VTH/RTH | แสดงด้วย | เอกสารบอก "ควรแสดงได้" + ได้คะแนนสมมติฐานชัดเจน |
| เกณฑ์ Saturation | `VCE ≤ 0.3 V` | ค่ามาตรฐานที่อธิบายได้ |
| เกณฑ์ Cutoff | `VTH ≤ VBE` | ตรวจได้จากค่า Thevenin โดยตรง |
| Validation | อยู่ใน `dc_bias.py` (ยกเว้น text→number อยู่ `app.py`) | เทสต์ได้โดยไม่ต้องผ่าน HTTP |
| HTTP status ตอน error | 400 + render หน้าเดิม | ถูกต้องตาม HTTP และยังเห็นฟอร์ม |
| ภาษา UI | ไทย (label + error) / symbol อังกฤษ | ผู้ตรวจเป็นคนไทย อ่านง่าย |
| ชื่อโหมด | `"Forward Active"`, `"Cutoff"`, `"Saturation"` | เป็นคำศัพท์เฉพาะทาง ไม่ต้องแปลซ้ำ |
| ตัวเลขใน dict | float หน่วย SI | แยกคณิตศาสตร์ออกจากการจัดรูปแบบ |
| จำนวนเทสต์ | 11 | เกินเกณฑ์ แต่ยังเขียนจบเร็ว |

---

## 7. สิ่งที่เหลือให้ผู้สร้าง (builder) ตัดสินเอง

- ค่า CSS จริง (สี, ระยะห่าง, เงา) — ขอให้อ่านง่ายและไม่ต้องใช้ CDN
- ถ้อยคำ warning ให้กระชับและตรงประเด็น (ต้องมีค่าตัวเลขประกอบ)
- จะแยกฟังก์ชันย่อยใน `dc_bias.py` หรือเขียนตรง ๆ ในฟังก์ชันเดียว (แนะนำ: เขียนตรง ๆ พร้อมคอมเมนต์)
- ลำดับการ์ดผลลัพธ์ และจะแสดง VTH/RTH ในการ์ดเดียวกันหรือแถวแยก
- รูปแบบตารางผลลัพธ์: grid หรือ `<table>` (แนะนำ `<table>` เพราะคัดลอกลงรายงานง่าย)

---

## 8. แผนตรวจรับ (A1–A7)

| # | เกณฑ์ | หลักฐานที่จะมี |
|---|---|---|
| A1 | เปิด `http://127.0.0.1:5000/` ได้ | `GET /` → 200 + ฟอร์ม |
| A2 | ผลมาจาก Python | `test_calculate_shows_results` + เปิดเว็บจริง |
| A3 | ค่าตรงคำนวณอิสระ | ตาราง §5.9 + `test_reference_values_forward_active` |
| A4 | Validation | 2 เทสต์ error + ลองกรอกเอง |
| A5 | เตือนนอก forward-active | `test_cutoff_when_vth_below_vbe`, `test_saturation_warns` |
| A6 | เทสต์ ≥ 3 + 1 | 11 เทสต์ |
| A7 | clone → run → test ได้ | README (มีอยู่แล้ว) + repo Public/เชิญอาจารย์ |

## 9. ความเสี่ยงที่รู้ตัว

| ความเสี่ยง | มาตรการ |
|---|---|
| repo ยังเป็น Private → อาจารย์ clone ไม่ได้ (A7 ตก) | ต้องเปลี่ยนเป็น Public หรือเพิ่ม collaborator ก่อนส่ง |
| ผู้ใช้อาจกรอก Ω แทน kΩ → ผลผิด 1000 เท่า | label ระบุ `(kΩ)` ชัด + README เตือน + ค่าเริ่มต้นเป็นตัวอย่างที่ถูก |
| ตอนสอบปากเปล่าอธิบาย saturation branch ไม่ได้ | เขียนคอมเมนต์ในโค้ดอธิบายเหตุผลไว้ทุกจุดที่ตัดสินใจ |
| ลืม push commit สุดท้าย | checklist §5 มีข้อ "Push commit ล่าสุดขึ้น GitHub แล้ว" |
| ยังไม่มี `docs/reflection.md` | อยู่นอกขอบเขตเอกสารนี้ — ถ้าอาจารย์ต้องการ ต้องแจ้งเพิ่ม |

## 10. ลำดับการทำงานหลังจากอนุมัติ

1. `writing-plans` → แผนทีละขั้นพร้อมจุดตรวจ
2. เขียน `dc_bias.py` → เทสต์สมการ (แดง → เขียว)
3. เขียน `app.py` + `templates/index.html` + `static/style.css`
4. เขียน `tests/test_web.py`
5. รัน `python -m unittest discover -s tests -v` ให้ผ่านทั้งหมด
6. เปิดเว็บจริง ตรวจด้วยตา + ถ่ายภาพหน้าจอ
7. ผู้ใช้ commit + push ผ่าน **GitHub Desktop** (ผมเตรียมข้อความ commit ให้)
8. เก็บ Repository URL + Commit SHA + ภาพหน้าจอ + Test Log ส่ง Moodle
