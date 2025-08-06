import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig(({mode}) => ({
  plugins: [
    react(),
  ],
  assetsInclude: ["**/*.PNG"],
  server: {
    open: true,
    proxy: {
      "/api": "http://127.0.0.1:2911",
    },
  },
}));
