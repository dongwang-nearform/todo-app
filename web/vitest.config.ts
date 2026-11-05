import react from '@vitejs/plugin-react'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    include: ['src/**/*.test.ts', 'src/**/*.test.tsx'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/api/client.ts', 'src/main.tsx', 'src/**/*.test.ts', 'src/**/*.test.tsx'],
      thresholds: {
        lines: 70,
        statements: 70,
        functions: 70,
      },
    },
  },
})
