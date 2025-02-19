import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(),
    tailwindcss(),
  ],

  // This ensures that when you run npm run build, Vite places the CSS and JS  files in the correct location that Django expects.

  build: {
    outDir: '../backend/static',  // Output to Django's static folder
    assetsDir: 'assets',  // Put all static assets in an 'assets' directory
  },

})
