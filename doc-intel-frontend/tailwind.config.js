/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",  // ✅ Tailwind will scan all these files for class names
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
