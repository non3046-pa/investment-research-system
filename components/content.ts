import { Locale } from "./types";

export const content: Record<Locale, any> = {
  th: {
    nav: { home: "หน้าแรก", about: "เกี่ยวกับ", products: "เมนู", experience: "ประสบการณ์", contact: "ติดต่อ" },
    hero: {
      title: "ประชุมสุข",
      subtitle: "กาแฟ พื้นที่พักใจ และแรงบันดาลใจสำหรับชีวิตที่สมดุล",
      ctaPrimary: "ดูเพิ่มเติม",
      ctaSecondary: "ติดต่อเรา",
    },
    about: {
      title: "เกี่ยวกับประชุมสุข",
      description:
        "ประชุมสุข คือพื้นที่ที่ออกแบบมาเพื่อการพักใจอย่างมีคุณภาพ เราผสมผสานกาแฟที่พิถีพิถัน แนวคิดการดูแลสุขภาพ การพัฒนาตนเอง และบทสนทนาที่มีความหมายเรื่องชีวิตและการเงินอย่างสมดุล เพื่อให้ทุกช่วงเวลาที่นี่ช่วยเติมพลังให้คุณก้าวต่อไปอย่างมั่นคง",
    },
    products: {
      title: "เมนูแนะนำ",
      items: ["Signature Coffee", "Healthy Tea", "Mindful Drink", "Inspiration Set"],
      descriptions: [
        "กาแฟซิกเนเจอร์รสชาตินุ่มลึกจากเมล็ดคัดพิเศษ",
        "ชาสมุนไพรและชาเบลนด์สำหรับคนใส่ใจสุขภาพ",
        "เครื่องดื่มเบาสบายที่ช่วยให้คุณอยู่กับปัจจุบัน",
        "เซ็ตเครื่องดื่มและของว่างสำหรับช่วงเวลาสร้างแรงบันดาลใจ",
      ],
      more: "ดูเพิ่มเติม",
    },
    experience: {
      title: "ประสบการณ์ที่คุณจะได้รับ",
      points: ["พื้นที่สงบ", "เครื่องดื่มคุณภาพ", "มุมสนทนาและแรงบันดาลใจ", "กิจกรรมด้านสุขภาพและการพัฒนาตนเอง"],
    },
    contact: { title: "ติดต่อเรา", name: "ชื่อ", phone: "เบอร์โทร", email: "อีเมล", message: "ข้อความ", submit: "ส่งข้อความ" },
    footer: { tagline: "กาแฟ สุขภาพ และแรงบันดาลใจในพื้นที่เดียว" },
  },
  en: {
    nav: { home: "Home", about: "About", products: "Products", experience: "Experience", contact: "Contact" },
    hero: {
      title: "PrachumSuk",
      subtitle: "Coffee, calm moments, and inspiration for a balanced life.",
      ctaPrimary: "Explore",
      ctaSecondary: "Contact Us",
    },
    about: {
      title: "About PrachumSuk",
      description:
        "PrachumSuk is a thoughtfully curated space where premium coffee, wellness, personal growth, and meaningful conversations about life and finance come together in balance.",
    },
    products: {
      title: "Featured Menu",
      items: ["Signature Coffee", "Healthy Tea", "Mindful Drink", "Inspiration Set"],
      descriptions: [
        "A smooth and rich house signature crafted from selected beans.",
        "Herbal and blended tea choices for mindful wellness.",
        "A light drink experience designed for clarity and calm.",
        "A drink-and-snack set made for inspired conversations.",
      ],
      more: "Learn More",
    },
    experience: {
      title: "Experience Highlights",
      points: ["Calm Space", "Quality Beverages", "Conversation & Inspiration Corner", "Wellness & Self-Development Activities"],
    },
    contact: { title: "Contact Us", name: "Name", phone: "Phone", email: "Email", message: "Message", submit: "Send Message" },
    footer: { tagline: "Coffee, wellness, and inspiration in one place." },
  },
};
