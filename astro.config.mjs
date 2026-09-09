import { defineConfig } from "astro/config";
import vercel from "@astrojs/vercel";

export default defineConfig({
  site: "https://greenlightbuyingmachine.com",
  output: "static",
  adapter: vercel(),
  trailingSlash: "never",
  build: { format: "file" },
});
