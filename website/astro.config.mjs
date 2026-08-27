import { defineConfig } from "astro/config";

const base = process.env.BASE_PATH || "/";

export default defineConfig({
  output: "static",
  base,
  site: process.env.SITE_URL || "https://highperformanceailab.github.io",
  build: {
    assets: "assets",
  },
});
