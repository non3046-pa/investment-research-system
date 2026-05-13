"use client";

import { Locale } from "./types";
import { content } from "./content";

export function Navbar({ locale, setLocale }: { locale: Locale; setLocale: (l: Locale) => void }) {
  const t = content[locale];
  return (
    <header className="sticky top-0 z-50 border-b border-gray-100 bg-white/90 backdrop-blur">
      <nav className="section-shell flex items-center justify-between py-4 md:py-5" aria-label="Main Navigation">
        <a href="#home" className="text-lg font-semibold">{locale === "th" ? "ประชุมสุข" : "PrachumSuk"}</a>
        <div className="hidden gap-6 md:flex text-sm">
          <a href="#home">{t.nav.home}</a><a href="#about">{t.nav.about}</a><a href="#products">{t.nav.products}</a><a href="#experience">{t.nav.experience}</a><a href="#contact">{t.nav.contact}</a>
        </div>
        <div className="rounded-full border border-gray-200 p-1 text-xs">
          <button className={`px-3 py-1 ${locale === "th" ? "text-premiumGold" : "text-gray-500"}`} onClick={() => setLocale("th")}>TH</button>
          <button className={`px-3 py-1 ${locale === "en" ? "text-premiumGold" : "text-gray-500"}`} onClick={() => setLocale("en")}>EN</button>
        </div>
      </nav>
    </header>
  );
}

export function Sections({ locale }: { locale: Locale }) {
  const t = content[locale];
  return (
    <>
      {/* Hero Section */}
      <section id="home" className="section-shell flex min-h-[72vh] flex-col justify-center text-center">
        <p className="text-sm uppercase tracking-[0.2em] text-minimalGreen">Lifestyle Café</p>
        <h1 className="mt-5 text-5xl font-semibold md:text-7xl">{t.hero.title}</h1>
        <p className="mx-auto mt-5 max-w-2xl text-lg text-gray-600">{t.hero.subtitle}</p>
        <div className="mt-10 flex flex-wrap justify-center gap-4">
          <a href="#about" className="rounded-full bg-premiumGold px-8 py-3 text-white">{t.hero.ctaPrimary}</a>
          <a href="#contact" className="rounded-full border border-gray-300 px-8 py-3">{t.hero.ctaSecondary}</a>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="section-shell border-t border-gray-100">
        <h2 className="text-3xl font-semibold md:text-4xl">{t.about.title}</h2>
        <p className="mt-6 max-w-4xl leading-8 text-gray-700">{t.about.description}</p>
      </section>

      {/* Products Section */}
      <section id="products" className="section-shell border-t border-gray-100">
        <h2 className="text-3xl font-semibold md:text-4xl">{t.products.title}</h2>
        <div className="mt-8 grid gap-6 md:grid-cols-2">
          {t.products.items.map((item: string, i: number) => (
            <article key={item} className="rounded-2xl border border-gray-100 bg-gray-50/60 p-6">
              <h3 className="text-2xl font-medium">{item}</h3>
              <p className="mt-3 text-gray-600">{t.products.descriptions[i]}</p>
              <button className="mt-6 text-sm font-medium text-minimalGreen">{t.products.more} →</button>
            </article>
          ))}
        </div>
      </section>

      {/* Experience Section */}
      <section id="experience" className="section-shell border-t border-gray-100">
        <h2 className="text-3xl font-semibold md:text-4xl">{t.experience.title}</h2>
        <ul className="mt-8 grid gap-4 md:grid-cols-2">
          {t.experience.points.map((point: string) => (
            <li key={point} className="rounded-xl border border-gray-100 p-5">• {point}</li>
          ))}
        </ul>
      </section>

      {/* Contact Section */}
      <section id="contact" className="section-shell border-t border-gray-100">
        <h2 className="text-3xl font-semibold md:text-4xl">{t.contact.title}</h2>
        <form className="mt-8 grid gap-4 md:max-w-2xl" onSubmit={(e) => e.preventDefault()}>
          <input className="rounded-xl border border-gray-200 p-3" placeholder={t.contact.name} />
          <input className="rounded-xl border border-gray-200 p-3" placeholder={t.contact.phone} />
          <input type="email" className="rounded-xl border border-gray-200 p-3" placeholder={t.contact.email} />
          <textarea className="min-h-32 rounded-xl border border-gray-200 p-3" placeholder={t.contact.message} />
          <button type="submit" className="w-fit rounded-full bg-minimalGreen px-8 py-3 text-white">{t.contact.submit}</button>
        </form>
      </section>
    </>
  );
}

export function Footer({ locale }: { locale: Locale }) {
  const t = content[locale];
  return (
    <footer className="border-t border-gray-100 bg-white">
      <div className="section-shell py-10">
        <p className="text-lg font-semibold">{locale === "th" ? "ประชุมสุข" : "PrachumSuk"}</p>
        <p className="mt-2 text-sm text-gray-600">{t.footer.tagline}</p>
        <div className="mt-4 flex gap-4 text-sm text-gray-600">
          <a href="#home">Home</a><a href="#about">About</a><a href="#products">Products</a><a href="#contact">Contact</a>
        </div>
      </div>
    </footer>
  );
}
