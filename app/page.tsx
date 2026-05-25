"use client";

import { useState } from "react";
import { Footer, Navbar, Sections } from "@/components/sections";
import { Locale } from "@/components/types";

export default function HomePage() {
  const [locale, setLocale] = useState<Locale>("th");

  return (
    <main>
      <Navbar locale={locale} setLocale={setLocale} />
      <Sections locale={locale} />
      <Footer locale={locale} />
    </main>
  );
}
