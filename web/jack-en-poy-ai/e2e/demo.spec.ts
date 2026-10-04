import { expect, test } from '@playwright/test';

test('demo plays, counters repeated moves, and resets without an API', async ({ page }) => {
    const apiRequests: string[] = [];
    const browserErrors: string[] = [];
    page.on('request', request => { if (new URL(request.url()).pathname.startsWith('/api/')) apiRequests.push(request.url()); });
    page.on('pageerror', error => browserErrors.push(error.message));
    await page.addInitScript(() => { Math.random = () => 0; });
    await page.goto('/');
    await expect(page.getByRole('complementary', { name: 'Browser demo' })).toBeVisible();
    for (let round = 1; round <= 4; round++) {
        await page.getByRole('button', { name: 'Play rock' }).click();
        await expect(page.getByRole('button', { name: 'Play paper' })).toBeDisabled();
        await expect(page.getByText(`ROUND ${round}`, { exact: true })).toBeVisible();
    }
    await expect(page.getByRole('heading', { name: 'Computer wins', exact: true })).toBeVisible();
    await expect(page.getByText('rock vs paper', { exact: true })).toBeVisible();
    await expect(page.getByText('Countering repeated moves', { exact: true })).toBeVisible();
    await expect(page.getByTestId('computer-score')).toHaveText('1');
    await expect(page.getByTestId('draw-score')).toHaveText('3');
    await page.locator('summary').click();
    await expect(page.getByText('1 rounds countering repeated moves', { exact: true })).toBeVisible();
    await page.screenshot({ path: 'test-results/browser-demo.png', fullPage: true });
    await page.getByRole('button', { name: 'New game' }).click();
    await expect(page.getByRole('heading', { name: 'Make your move.' })).toBeVisible();
    await expect(page.getByTestId('computer-score')).toHaveText('0');
    await page.keyboard.press('p');
    await expect(page.getByText('ROUND 1', { exact: true })).toBeVisible();
    expect(apiRequests).toEqual([]);
    expect(browserErrors).toEqual([]);
});

test('demo fits a phone viewport and accepts a move', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/');
    await expect(page.getByRole('button', { name: 'Play scissors' })).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    await page.getByRole('button', { name: 'Play scissors' }).click();
    await expect(page.getByText('ROUND 1', { exact: true })).toBeVisible();
    await page.screenshot({ path: 'test-results/browser-demo-mobile.png', fullPage: true });
});
