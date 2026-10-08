/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#0B1F3A',
          800: '#142C4C',
          700: '#1E3A5F',
        },
        solar: {
          green: '#10B981',
          yellow: '#F59E0B',
          amber: '#D97706',
        }
      }
    },
  },
  plugins: [],
}
