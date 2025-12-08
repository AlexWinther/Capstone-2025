/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Match old design system
        primary: {
          DEFAULT: "#007bff",
          dark: "#0056b3",
          light: "#4f8cff",
        },
        text: {
          primary: "#1a237e",
          secondary: "#222",
          muted: "#495057",
          light: "#6c757d",
        },
        background: {
          DEFAULT: "#f7fafd",
          start: "#e3e9f0",
        },
      },
      borderRadius: {
        lg: "18px",
        xl: "24px",
        "2xl": "28px",
        "3xl": "32px",
      },
      backdropBlur: {
        xs: "2px",
      },
      boxShadow: {
        glass: "0 8px 32px 0 rgba(31, 38, 135, 0.10)",
        "glass-lg": "0 16px 48px 0 rgba(0,123,255,0.18)",
      },
    },
  },
  plugins: [],
}
