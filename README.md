# Xerl-Tiktok — TikTok LIVE แจ้งเตือน Discord (Embed + ปุ่มกดดูไลฟ์)

บอทตัวนี้จะตรวจจับการเริ่ม LIVE ของ TikTok แล้วส่งแจ้งเตือนเข้า Discord เป็น Embed สวย ๆ พร้อมปุ่ม “กดเข้าดูไลฟ์” และลิงก์ไลฟ์

## ฟีเจอร์
- แจ้งเตือนเมื่อเริ่ม LIVE (Embed สวย ๆ)
- มีปุ่มกดเข้าดูไลฟ์ (Link Button)
- แจ้งเตือนเมื่อ LIVE จบ
- รันบน Windows / VPS / Railway ได้
- ตั้งค่าทั้งหมดผ่าน `.env` (ไม่ต้องแก้โค้ด)

---

## โครงสร้างไฟล์
- `main.py` — ตัวบอทหลัก
- `requirements.txt` — dependencies
- `.env` — config (ห้ามอัปขึ้น GitHub)
- `.gitignore` — กันไฟล์ลับขึ้น repo

---

## ติดตั้งและรันบนเครื่อง (Local)

### 1) ติดตั้ง Python
แนะนำ Python 3.11 หรือ 3.12 (ถ้าใช้ 3.14 ก็รันได้ แต่บางไลบรารีอาจจุกจิก)

เช็คเวอร์ชัน:
```bash
python --version
