# ประชุมสุข (PrachumSuk) Landing Page

เว็บไซต์ One Page สำหรับแบรนด์ “ประชุมสุข” พัฒนาด้วย **Next.js + React + Tailwind CSS**

## วิธีติดตั้งแบบง่ายมาก

1. เปิด Terminal ในโฟลเดอร์โปรเจกต์นี้
2. ติดตั้งโปรแกรมที่จำเป็นก่อน:
   - ติดตั้ง [Node.js LTS](https://nodejs.org/) (แนะนำเวอร์ชัน 20 ขึ้นไป)
3. ติดตั้งแพ็กเกจ:

```bash
npm install
```

4. รันเว็บไซต์โหมดพัฒนา:

```bash
npm run dev
```

5. เปิดเบราว์เซอร์ไปที่:

```text
http://localhost:3000
```

## คำสั่งที่ใช้บ่อย

- `npm run dev` เริ่มโปรเจกต์
- `npm run build` สร้างไฟล์สำหรับ production
- `npm run start` รันโปรเจกต์แบบ production

## โครงสร้างหลัก

- `app/page.tsx` หน้า Landing Page หลัก
- `components/sections.tsx` ส่วน Navbar, Hero, About, Products, Experience, Contact, Footer
- `components/content.ts` ข้อความสองภาษา TH/EN
- `app/layout.tsx` metadata พื้นฐาน SEO
