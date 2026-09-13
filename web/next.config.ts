import type { NextConfig } from 'next';
// Set BASE_PATH=/maniac-mansion when building for a subdirectory.
// An unset value keeps the existing localhost/root deployment.
const rawBasePath = process.env.BASE_PATH?.trim() || '';
const basePath = rawBasePath === '/' ? '' : rawBasePath.replace(/\/+$/, '');
if (basePath && (!basePath.startsWith('/') || basePath.startsWith('//') || /[?#\\\s]/.test(basePath) || basePath.split('/').some(part => part === '.' || part === '..'))) {
  throw new Error('BASE_PATH must be an absolute URL path, for example /maniac-mansion');
}
const nextConfig: NextConfig = {
  output: 'export',
  basePath,
  env: { NEXT_PUBLIC_BASE_PATH: basePath },
};
export default nextConfig;
