# AGENTS.md — กติกาการเขียนโค้ดใน repo นี้

โปรเจกต์: BJT DC Bias Web App (ENG29 2121 Lab 02)
ไฟล์นี้ใช้เป็นแนวทางสำหรับทุกคน (รวม AI assistant) ที่แก้ไขโค้ดใน repo

## โครงไฟล์ที่ต้องรักษา

```
app.py              Flask routes + อ่านฟอร์ม (รู้จัก Flask ได้)
dc_bias.py          สมการวิศวกรรม + validation (ห้าม import Flask)
templates/index.html หน้าฟอร์ม + แสดงผล (Jinja, ภาษาไทย)
static/style.css    ตัวหน้าตา (ไม่มี JavaScript, ไม่มี CDN)
tests/              unit tests (test_dc_bias.py) + Flask client tests (test_web.py)
docs/               design-note.md, validation.md, reflection.md, test-log.txt, checklist.md
AGENTS.md           ไฟล์นี้ (กติกาการเขียนโค้ด)
README.md           ติดตั้ง / รัน / ทดสอบ + สมการ + ค่าอ้างอิง
```

## กติกาที่ห้ามละเมิด

1. **ห้ามใส่ JavaScript** — หน้าต้องทำงานได้ด้วย HTML ฟอร์ม + Flask เท่านั้น
2. **ห้ามให้ `dc_bias.py` import Flask** — สมการต้องทดสอบได้โดยไม่ต้องเปิด HTTP
3. **ตัวต้านทานกรอกเป็น kΩ** — backend คูณ 1000 ภายใน `dc_bias.py` เท่านั้น label แสดง `(kΩ)`
4. **ชื่อตัวแปรตรงกับสมการในเอกสาร Lab** — `VTH`, `RTH`, `IB`, `IC`, `IE`, `VB`, `VE`, `VC`, `VCE`
5. **คืนผลเป็น `dict` จาก `calculate_dc_bias(...)`** — ห้ามใช้ dataclass / class สำหรับผลลัพธ์
6. **ทุกค่าที่แสดงใน template ต้องมีหน่วยกำกับ** (V, mA, µA, kΩ)
7. **ไม่ commit** `.venv/`, `__pycache__/`, `.env`, `*.log`
8. **ข้อความ error/warning เป็นภาษาไทย** อ่านรู้เรื่อง ระบุชื่อฟิลด์ที่ผิด
9. **ถ้าแก้สมการ ต้องเพิ่ม/แก้ unit test คู่กัน** — ทดสอบก่อนแก้ (TDD)

## คำสั่งที่ใช้บ่อย

```powershell
# รันเซิร์ฟเวอร์
.\\.venv\\Scripts\\python.exe -m flask --app app run --debug

# รันทดสอบทั้งหมด
.\\.venv\\Scripts\\python.exe -m unittest discover -s tests -v

# ดูสถานะ git
git status --short --branch