import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://visualanalyticshealthcare.github.io',
  base: '/homepage',
  output: 'static',
  build: {
    format: 'directory'
  }
});
