/** Work around the installed vinext exporter's basePath handling for this single-page app.
 * It probes / rather than basePath and emits framework assets under the prefix.
 * Produce a self-contained folder whose contents can be uploaded into that prefix.
 */
import { access, writeFile, rename } from 'node:fs/promises';
const { default: render, __basePath: basePath } = await import('../dist/server/index.js');
const target = new URL('../dist/client/index.html', import.meta.url);
try { await access(target); } catch {
  if (!basePath) throw new Error('Static build is missing index.html');
  const response = await render(new Request(`http://localhost${basePath}/`));
  if (response.status !== 200 || !response.headers.get('content-type')?.includes('text/html')) {
    throw new Error(`Could not export ${basePath}/: HTTP ${response.status}`);
  }
  const html = await response.text();
  if (!html.includes('<html')) throw new Error('Static export did not return an HTML document');
  await writeFile(target, html);
  console.log(`Exported static index.html for ${basePath}/`);
}
if (basePath) {
  const nested = new URL(`../dist/client${basePath}/_next`, import.meta.url);
  // Already-normalized output is left alone, making this step safe to rerun.
  let exists = false;
  try { await access(nested); exists = true; } catch {}
  if (exists) await rename(nested, new URL('../dist/client/_next', import.meta.url));
}
