import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import * as path from "node:path";

export default defineConfig({
  plugins: [vue()],
  esbuild: {
    loader: "ts",
    target: "esnext"
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: "index.js",
        chunkFileNames: "assets/[name]-[hash].js",
        assetFileNames: "assets/[name]-[hash][extname]"
      }
    }
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
});
