/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        brand: {
          burgundy: '#774737',
          'burgundy-dark': '#5e382b',
          'burgundy-light': '#905644',
          cyan: '#a3e9ec',
          'cyan-dark': '#5bbbc0',
          sand: '#cbb8a9',
          'sand-light': '#f3eee9',
          slate: '#32393c',
          olive: '#b1ac90',
          'olive-muted': '#aba88b',
          border: '#e0dbd3',
          card: '#ffffff',
          body: '#f4f3ef',
        }
      },
      fontFamily: {
        heading: ['Segoe UI', 'Tahoma', 'Arial', 'Helvetica Neue', 'sans-serif'],
        body: ['Segoe UI', 'Roboto', 'Arial', 'sans-serif'],
      }
    },
  },
  corePlugins: {
    preflight: false,
  },
  plugins: [],
};
