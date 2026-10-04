import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig(({ mode }) => ({
    base: loadEnv(mode, process.cwd(), '').VITE_BASE_PATH || '/',
    build: { outDir: mode === 'demo' ? 'dist-demo' : 'dist' },
    plugins: [react(), tailwindcss()],
    server: { host: '127.0.0.1', strictPort: true, proxy: { '/api': { target: 'http://127.0.0.1:8080', changeOrigin: true } } },
    preview: { host: '127.0.0.1', strictPort: true, proxy: { '/api': { target: 'http://127.0.0.1:8080', changeOrigin: true } } },
}));
