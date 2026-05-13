import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ประชุมสุข | Lifestyle Café & Inspiration Space",
  description:
    "ประชุมสุข คาเฟ่สำหรับการพักใจ ดื่มกาแฟคุณภาพ และรับแรงบันดาลใจด้านสุขภาพ การพัฒนาตนเอง และการวางแผนชีวิต",
  keywords: ["ประชุมสุข", "คาเฟ่", "กาแฟ", "สุขภาพ", "แรงบันดาลใจ", "lifestyle cafe"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="th">
      <body>{children}</body>
    </html>
  );
}
