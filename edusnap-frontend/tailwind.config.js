/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#1E40AF",  // Blue
        secondary: "#F3F4F6", // Light gray/white
        accent: "#3B82F6",   // Subtle AI accent
      },
    },
  },
  plugins: [],
};