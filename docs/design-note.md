# Design Note — BJT DC Bias Web App

ENG29 2121 Lab 02 · Flask + Python
วันที่จัดทำ: 2026-11-10

## โครงการ

เว็บแอปหน้าเดียว คำนวณจุดทำงาน DC (DC operating point) ของ BJT ต่อแบบ
Common-Emitter with voltage-divider bias แสดงผล VB, VE, VC, VCE, IC (รวม IB, IE)
พร้อมหน่วย และแจ้งเตือนเมื่อไม่อยู่ในโหมด forward-active

## โครงสร้างไฟล์

| ไฟล์ | หน้าที่ |
|---|---|
| `app.py` | Flask routes (`GET /`, `POST /calculate`) อ่านฟอร์ม เรียกสมการ แสดงผล |
| `dc_bias.py` | สมการวิศวกรรม + validation (ไม่รู้จัก Flask) |
| `templates/index.html` | ฟอร์มภาษาไทย + ตารางผลลัพธ์ (Jinja) |
| `static/style.css` | ตัวหน้าตา (ไม่มี JavaScript, ไม่มี CDN) |
| `tests/test_dc_bias.py` | Unit tests ของสมการ 8 ทดสอบ |
| `tests/test_web.py` | Flask test client 4 ทดสอบ |
| `docs/` | design-note, validation, reflection, test-log, checklist |

## แนวทางการออกแบบที่เลือก

### 1. หน่วยตัวต้านทาน = kΩ (Approach A)
ผู้ใช้กรอก `R1 = 100` ในช่อง `R1 (kΩ)` backend คูณ 1000 ภายใน `dc_bias.py`
ตรงกับค่าตัวอย่างในเอกสาร Lab (100k, 22k, 2.2k, 1k) ลดโอกาสพิมพ์เลขศูนย์ผิด

### 2. ฟังก์ชันเดียวคืน `dict` (Approach A)
`calculate_dc_bias(vcc, r1, r2, rc, re, beta, vbe) -> dict`
ไม่ใช้ dataclass / class เพื่อให้อธิบายได้ทุกบรรทัดตอนตอบคำถามรายบุคคล และส่งค่าเข้า Jinja template ได้ตรง ๆ

### 3. ตรวจโหมดการทำงาน
- `VTH ≤ VBE` → **Cutoff**: กระแสเป็นศูนย์ คำนวณถูกต้องทันที
- `VCE ≤ 0.3 V` → **Saturation**: คงตัวเลข Forward-Active ไว้ พร้อมข้อความเตือนว่าใช้สมการนี้ไม่ได้ในโหมดอิ่มตัว (สมมติ VCE_sat เพิ่มเติมอยู่นอกขอบเขต Lab)
- อื่น → **Forward Active**

### 4. Validation
ตรวจ `VCC, R1, R2, RC, RE, β, VBE` ตามลำดับ ค่าติดลบ / ศูนย์ / ข้อความไม่ใช่ตัวเลข → `ValueError` ภาษาไทย ระบุชื่อฟิลด์ Flask คืน HTTP 400 พร้อมคงค่าที่ผู้ใช้พิมพ์ไว้

## ค่าอ้างอิง (ทดสอบแล้ว)

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

## ข้อจำกัดที่รู้ตัว

- Saturation branch คงตัวเลข Forward-Active ไว้ + ข้อความเตือน (ยังไม่คำนวณ VCE_sat จริง)
- ไม่มี JavaScript / กราฟ / AC analysis ตามขอบเขต Lab
- commit ต้องทำผ่าน GitHub Desktop (ผู้ใช้เป็นผู้กด)
