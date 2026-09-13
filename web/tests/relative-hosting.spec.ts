import { test, expect } from '@playwright/test';
import { mkdtemp, mkdir, readdir, symlink, copyFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawn, type ChildProcess } from 'node:child_process';
import { once } from 'node:events';

let directory: string, origin: string, server: ChildProcess;
const mounts = ['/', '/maniac-mansion-3d/', '/games/mansion/'];

test.beforeAll(async () => {
  directory = await mkdtemp(join(tmpdir(), 'mansion-relative-'));
  const root = join(directory, 'dist/client'), build = resolve('dist/client');
  await mkdir(join(root, 'games'), { recursive: true });
  // Every mount serves the same build files, without rebuilding or rewriting.
  for (const file of await readdir(build)) await symlink(join(build, file), join(root, file));
  await symlink(build, join(root, 'maniac-mansion-3d'));
  await symlink(build, join(root, 'games/mansion'));
  await copyFile('serve.mjs', join(directory, 'serve.mjs'));
  server = spawn(process.execPath, [join(directory, 'serve.mjs')], { env: { ...process.env, PORT: '0' }, stdio: ['ignore', 'pipe', 'pipe'] });
  origin = await new Promise<string>((accept, reject) => {
    let output = '';
    const timer = setTimeout(() => reject(new Error('Static server did not start')), 10000);
    server.once('error', error => { clearTimeout(timer); reject(error); });
    server.once('exit', code => { clearTimeout(timer); reject(new Error(`Static server exited: ${code}`)); });
    server.stdout!.on('data', chunk => {
      output += chunk.toString();
      const match = output.match(/http:\/\/127\.0\.0\.1:\d+/);
      if (match) { clearTimeout(timer); accept(match[0]); }
    });
  });
});

test.afterAll(async () => {
  if (server && server.exitCode === null) { const stopped = once(server, 'exit'); server.kill(); await stopped; }
  if (directory) await rm(directory, { recursive: true, force: true });
});

for (const mount of mounts) {
  test(`same static build loads and moves at ${mount}`, async ({ page, request }) => {
    const errors: string[] = [], resources: string[] = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('requestfailed', req => errors.push(`${req.url()}: ${req.failure()?.errorText}`));
    page.on('response', response => {
      if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`);
      if (['script', 'stylesheet'].includes(response.request().resourceType()) || /\.glb$/.test(response.url())) resources.push(response.url());
    });
    await page.addInitScript(() => { HTMLCanvasElement.prototype.requestPointerLock = () => Promise.reject(new Error('Use deterministic drag controls')); });
    await page.goto(`${origin}${mount}?room=hall`);
    await expect(page.getByRole('button', { name: 'Pause', exact: true })).toBeVisible({ timeout: 45000 });
    await expect(page.locator('canvas')).toBeVisible();
    const state = async () => JSON.parse((await page.locator('.viewport').getAttribute('data-walker'))!);
    const before = await state();
    await page.keyboard.down('w');
    try { await expect.poll(async () => { const p = await state(); return Math.hypot(p.x - before.x, p.y - before.y); }).toBeGreaterThan(.3); }
    finally { await page.keyboard.up('w'); }
    await page.keyboard.press('r');
    await expect.poll(async () => (await state()).x).toBeCloseTo(before.x, 2);
    // Look left toward the initially closed front door from the hall spawn.
    const reset = await state(), yaw = -Math.atan2(-6.4 - reset.x, 2.35 - reset.y);
    const drag = -(yaw - reset.yaw) / .0022;
    await page.mouse.move(1100, 450); await page.mouse.down(); await page.mouse.move(1100 + drag, 450, { steps: 5 }); await page.mouse.up();
    await expect.poll(async () => (await state()).yaw).toBeCloseTo(yaw, 2);
    await expect(page.locator('.door-action')).toContainText('Open');
    await page.locator('.door-action').click();
    await expect(page.locator('.door-action')).toContainText('Close');
    await page.reload();
    await expect(page.getByRole('button', { name: 'Pause', exact: true })).toBeVisible({ timeout: 45000 });
    const favicon = await page.locator('link[rel="icon"]').getAttribute('href');
    expect(new URL(favicon!, page.url()).pathname).toBe(`${mount}favicon.svg`);
    expect((await request.get(new URL(favicon!, page.url()).href)).ok()).toBe(true);
    expect(resources.some(url => url.endsWith('.glb'))).toBe(true);
    expect(resources.every(url => new URL(url).pathname.startsWith(mount))).toBe(true);
    expect(errors).toEqual([]);
  });
}

test('directory redirects preserve room queries and explicit index.html works', async ({ page, request }) => {
  for (const mount of mounts.slice(1)) {
    const response = await request.get(`${origin}${mount.slice(0, -1)}?room=kitchen`, { maxRedirects: 0 });
    expect(response.status()).toBe(308);
    expect(response.headers().location).toBe(`${mount}?room=kitchen`);
  }
  for (const mount of mounts) {
    await page.goto(`${origin}${mount}index.html?room=kitchen`);
    await expect(page.getByRole('heading', { name: 'Kitchen', exact: true })).toBeVisible({ timeout: 45000 });
    await expect(page.getByRole('button', { name: 'Pause', exact: true })).toBeVisible();
  }
});
