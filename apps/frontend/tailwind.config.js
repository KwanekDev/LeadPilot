/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dark cosmic palette
        cosmic: {
          950: "#0a0e27",
          900: "#0f172a",
          800: "#1e293b",
          700: "#334155",
          600: "#475569",
        },
        // Accent colors
        accent: {
          cyan: "#06b6d4",
          purple: "#a855f7",
          blue: "#3b82f6",
        },
        // Light text colors
        light: {
          primary: "#e2e8f0",
          secondary: "#cbd5e1",
          tertiary: "#94a3b8",
        },
      },
      backgroundColor: {
        cosmic: "#0f172a",
        "cosmic-dark": "#0a0e27",
        glass: "rgba(30, 41, 59, 0.5)",
      },
      backdropBlur: {
        xs: "2px",
        sm: "4px",
        md: "8px",
        lg: "12px",
        xl: "16px",
      },
      boxShadow: {
        "glow-blue": "0 0 20px rgba(59, 130, 246, 0.3), 0 0 40px rgba(59, 130, 246, 0.1)",
        "glow-purple": "0 0 20px rgba(168, 85, 247, 0.3), 0 0 40px rgba(168, 85, 247, 0.1)",
        "glow-cyan": "0 0 20px rgba(6, 182, 212, 0.3), 0 0 40px rgba(6, 182, 212, 0.1)",
        "glow-sm": "0 0 10px rgba(59, 130, 246, 0.2)",
      },
      backgroundImage: {
        "gradient-cosmic": "linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0a0e27 100%)",
        "gradient-glow-blue": "linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%)",
      },
      borderImage: {
        gradient: "linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)",
      },
      animation: {
        "glow-pulse": "glow-pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "float": "float 6s ease-in-out infinite",
        "shimmer": "shimmer 2s infinite",
      },
      keyframes: {
        "glow-pulse": {
          "0%, 100%": {
            opacity: "1",
            boxShadow: "0 0 20px rgba(59, 130, 246, 0.3)",
          },
          "50%": {
            opacity: "0.8",
            boxShadow: "0 0 30px rgba(59, 130, 246, 0.5)",
          },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-20px)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-1000px 0" },
          "100%": { backgroundPosition: "1000px 0" },
        },
      },
    },
  },
  plugins: [],
  darkMode: "class",
}
