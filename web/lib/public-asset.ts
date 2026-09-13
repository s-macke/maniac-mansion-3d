/** Public files are outside the framework asset pipeline; prefix them explicitly. */
export function publicAssetUrl(path: string, basePath = process.env.NEXT_PUBLIC_BASE_PATH || '') {
  return `${basePath}/${path.replace(/^\/+/, '')}`;
}
