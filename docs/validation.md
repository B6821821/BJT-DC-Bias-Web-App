# Validation Log — BJT DC Bias Web App

ENG29 2121 Lab 02 · บันทึกผลตรวจรับ (A3, A4, A5, A6)
วันที่: 2026-11-10 · ทดสอบด้วย Python 3.13.17 + Flask 3.1.3

## A3 — ค่าตรงกับคำนวณอิสระ

ชุดค่าอ้างอิง: `VCC=12, R1=100k, R2=22k, RC=2.2k, RE=1k, β=100, VBE=0.70`

| ปริมาณ | ค่าที่คำนวณ | ค่าอ้างอิง | ผล |
|---|---|---|---|
| VTH | 2.1639 V | 2.1639 V | ✅ |
| RTH | 18.0328 kΩ | 18.0328 kΩ | ✅ |
| IB | 12.299 µA | 12.299 µA | ✅ |
| IC | 1.2299 mA | 1.2299 mA | ✅ |
| IE | 1.2422 mA | 1.2422 mA | ✅ |
| VB | 1.9422 V | 1.9422 V | ✅ |
| VE | 1.2422 V | 1.2422 V | ✅ |
| VC | 9.2943 V | 9.2943 V | ✅ |
| VCE | 8.0522 V | 8.0522 V | ✅ |

รันจริงผ่าน Flask test client: `POST /calculate` → HTTP 200, หน้าแสดง `1.9422`, `Forward Active`

## A4 — Input Validation

| กรณีทดสอบ | ผลลัพธ์ที่คาดหวัง | ผลจริง |
|---|---|---|
| `VCC = 0` | ValueError "VCC ต้องมากกว่า 0 V" | ✅ |
| `R1 = 0` | ValueError "R1 ต้องมากกว่า 0 kΩ" | ✅ |
| `RC = 0` | ValueError "RC ต้องมากกว่า 0 kΩ" | ✅ |
| `RE = 0` | HTTP 400, หน้ามีคำว่า "RE", คงค่าที่กรอกไว้ | ✅ |
| `β = 0` | ValueError "β ต้องมากกว่า 0" | ✅ |
| `VBE = VCC` (เช่น 12) | ValueError "VBE ต้องมากกว่า 0 V และน้อยกว่า VCC" | ✅ |
| `VCC = abc` | HTTP 400, ข้อความบอกให้กรอกเป็นตัวเลข | ✅ |
| ช่องว่าง / empty | ValueError ระบุชื่อฟิลด์ | ✅ |

หน้าไม่ล้มทุกกรณี (ไม่มี 500 error จาก input ผิด)

## A5 — Warning เมื่อนอก forward-active

| กรณี | โหมดที่ตรวจได้ | ข้อความเตือน |
|---|---|---|
| `R1=100k, R2=4.7k` (VTH ≈ 0.54 V ≤ VBE) | Cutoff | มีคำว่า "Cutoff", IC = 0, VCE = VCC |
| `RC=10k` (VCE ≤ 0.3 V) | Saturation | มีคำว่า "Saturation", คำเตือนว่าสมการ Forward-Active ไม่ใช้บังคับ |

## A6 — Automated Tests

รัน: `python -m unittest discover -s tests -v`

| ไฟล์ | จำนวนทดสอบ | สถานะ |
|---|---|---|
| `tests/test_dc_bias.py` | 8 | ✅ ผ่านทั้งหมด |
| `tests/test_web.py` | 4 | ✅ ผ่านทั้งหมด |
| **รวม** | **12** | **✅ OK** |

เกณฑ์ขั้นต่ำ: unit tests ≥ 3 + Flask client ≥ 1 → ทำได้ 8 + 4 = 12 (เกินเกณฑ์)

## สรุป

ทดสอบรับครบทุกเกณฑ์ A3–A6 พร้อมส่งงาน
