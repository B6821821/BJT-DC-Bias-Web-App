# Checklist — ENG29 2121 Lab 02

BJT DC Bias Web App · Flask + Python
อัปเดต: 2026-11-10

---

## 1. ก่อนเริ่มใช้งาน (Pre-flight)

รันคำสั่งเหล่านี้ใน PowerShell ที่โฟลเดอร์โปรเจกต์

| # | รายการ | คำสั่งตรวจ | ค่าที่ต้องได้ | สถานะ |
|---|---|---|---|---|
| 1 | Git | `git --version` | 2.56.x | ✅ |
| 2 | Git identity | `git config --global --get user.name` | รุจาภา หงส์พนัส | ✅ |
| 3 | Git email | `git config --global --get user.email` | rujapha2461@gmail.com | ✅ |
| 4 | Python | `python --version` | 3.13.x | ✅ |
| 5 | venv | `.\.venv\Scripts\python.exe --version` | 3.13.x | ✅ |
| 6 | Flask | `.\.venv\Scripts\python.exe -m flask --version` | 3.1.3 | ✅ |
| 7 | OpenCode Desktop | About / Settings | 2.2.6 | ✅ |
| 8 | Superpowers | `use skill tool to list skills` | เห็น `brainstorming` | ✅ |
| 9 | GitHub Desktop | เปิดแอป + ล็อกอิน | เห็น repo ในแถบซ้าย | ✅ |
| 10 | Publish repo | `git remote -v` | มี `origin` | ⬜ ยังไม่มี |
| 11 | `.venv` ถูก ignore | `git check-ignore -v .venv/` | `.gitignore:8:.venv/` | ✅ |

### ถ้าข้อไหนไม่ผ่าน

```powershell
# Git ยังไม่ติดตั้ง
winget install --id Git.Git -e

# Python ยังไม่ติดตั้ง
winget install --id Python.Python.3.13 -e --override "/quiet InstallAllUsers=0 PrependPath=1 Include_pip=1"

# ยังไม่มี venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

---

## 2. Publish repo ขึ้น GitHub (ครั้งเดียว)

GitHub Desktop → `File` → `Publish repository…`

| ช่อง | ค่า |
|---|---|
| Name | `BJT-DC-Bias-Web-App` |
| Description | `Flask BJT DC bias calculator — ENG29 2121 Lab 02` |
| Keep this code private | ไม่ติ๊ก (ให้อาจารย์ clone ได้ตามเกณฑ์ A7) |

กด **Publish repository** → ระบบ push commit ที่มีอยู่ขึ้นไปให้อัตโนมัติ

ตรวจว่าได้ผล:
```powershell
git remote -v
git push -u origin main
```

---

## 3. Commit ด้วย GitHub Desktop (ใช้ทุกครั้ง)

1. เปิด GitHub Desktop → เลือก repo `BJT DC Bias Web App`
2. แท็บ **Changes** → ตรวจรายการไฟล์
3. คลิกแต่ละไฟล์ → อ่าน diff ทางขวา
4. ตรวจว่า **ไม่มี** `.venv/`, `__pycache__/`, `.env`
5. ช่อง **Summary** → เขียนข้อความสั้น ๆ ว่าเปลี่ยนอะไร
6. ช่อง **Description** (ถ้ามี) → ใส่รายละเอียดเป็นข้อ ๆ
7. กด **Commit to main**
8. กด **Push origin** (มุมขวาบน)

### ข้อความ commit ที่แนะนำ

| งาน | Summary |
|---|---|
| สมการ + unit tests | `Add dc_bias module with unit tests` |
| Flask routes | `Add Flask routes for DC bias form` |
| Template + CSS | `Add index template and stylesheet` |
| Flask client test | `Add Flask route tests` |
| Validation / warning | `Handle invalid input and region warnings` |
| เอกสาร | `Add design note and validation log` |

### ข้อห้าม

| อย่าทำ | ผลที่เกิด |
|---|---|
| กด **Discard changes** | ลบงานที่แก้ทิ้งถาวร กู้คืนไม่ได้ |
| Commit โดยไม่ดู diff | อาจหลุด `.env`, API key, ไฟล์ขยะ |
| ลืม **Push origin** | งานไม่อยู่บน GitHub อาจารย์ตรวจไม่ได้ |
| Commit `.venv/` | ผิดกฎ Lab และ repo บวมหลายสิบ MB |

---

## 4. เกณฑ์ตรวจรับ (A1–A7)

| # | รายการ | ต้องเห็นอะไร |
|---|---|---|
| A1 | `GET /` | เปิด `http://127.0.0.1:5000/` ได้ HTTP 200 เห็นฟอร์ม |
| A2 | `POST /calculate` | กรอกค่าแล้วได้ผลจาก Python จริง ไม่ใช่ค่าฮาร์ดโค้ด |
| A3 | Engineering reference | VB, VE, VC, VCE, IC ตรงกับคำนวณอิสระ |
| A4 | Validation | R≤0, β≤0, ค่าไม่ใช่ตัวเลข → error ชัดเจน หน้าไม่ล้ม |
| A5 | Outside active region | เตือน Cutoff / Saturation |
| A6 | Tests | ≥3 unit tests + ≥1 Flask test client test |
| A7 | GitHub reproducibility | clone → install → run → test ตาม README ได้ |

### ค่าอ้างอิงสำหรับตรวจ A3

`VCC=12, R1=100k, R2=22k, RC=2.2k, RE=1k, β=100, VBE=0.70`

| ปริมาณ | ค่า |
|---|---|
| VB | 1.9422 V |
| VE | 1.2422 V |
| VC | 9.2943 V |
| VCE | 8.0522 V |
| IC | 1.2299 mA |

---

## 5. ก่อนส่งงาน

- [ ] `python -m unittest discover -s tests -v` ผ่านทั้งหมด
- [ ] เปิดเว็บ demo ได้จริง และคำนวณถูก
- [ ] ลองกรอกค่าผิด → เห็น error
- [ ] `git status` สะอาด (ไม่มีไฟล์ค้าง)
- [ ] Push commit ล่าสุดขึ้น GitHub แล้ว
- [ ] คัดลอก **Repository URL**
- [ ] คัดลอก **Commit SHA** (History → คลิกขวา → Copy SHA)
- [ ] ภาพหน้าจอเว็บที่คำนวณสำเร็จ
- [ ] Test Log
- [ ] `README.md` อธิบายวิธีติดตั้ง/รัน/ทดสอบครบ
- [ ] `docs/reflection.md` เขียนครบ

ส่งทาง Moodle: Repository URL + Commit SHA + ภาพหน้าจอ + Test Log
