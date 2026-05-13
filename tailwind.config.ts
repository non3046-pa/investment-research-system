import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        premiumGold: "#C8A45D",
        minimalGreen: "#6B8F71",
        inkDark: "#1F2933",
      },
      fontFamily: {
        sans: ["Inter", "Prompt", "Noto Sans Thai", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
