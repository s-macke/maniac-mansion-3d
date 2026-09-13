/** Resolve public files beside index.html, wherever the site folder is hosted. */
export function publicAssetUrl(path: string) {
  return `./${path.replace(/^\/+/, '')}`;
}
