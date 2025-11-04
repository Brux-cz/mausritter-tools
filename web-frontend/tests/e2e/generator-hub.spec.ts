import { test, expect } from '@playwright/test';

test.describe('Generator Hub', () => {
  test('should load generator hub page', async ({ page }) => {
    await page.goto('/generators');
    await expect(page.locator('h1')).toContainText('Generátory');
  });

  test('should display all 17 generators', async ({ page }) => {
    await page.goto('/generators');

    // Count generator cards
    const cards = page.locator('a').filter({ has: page.locator('[class*="Card"]') });
    const count = await cards.count();
    expect(count).toBe(17);
  });

  test('should display filter buttons', async ({ page }) => {
    await page.goto('/generators');

    await expect(page.getByRole('button', { name: /Všechny/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /MVP/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /Extended/i })).toBeVisible();
  });

  test('should filter by MVP category', async ({ page }) => {
    await page.goto('/generators');

    // Click MVP filter
    await page.getByRole('button', { name: /MVP \(5\)/i }).click();

    // Should show 5 generators
    const cards = page.locator('a').filter({ has: page.locator('[class*="Card"]') });
    const count = await cards.count();
    expect(count).toBe(5);
  });

  test('should have working search functionality', async ({ page }) => {
    await page.goto('/generators');

    // Search for "Character"
    await page.getByPlaceholder(/Hledat generátor/i).fill('Character');

    // Should show only Character generator
    await expect(page.getByText('Character Generator')).toBeVisible();
  });

  test('should link to Character generator page', async ({ page }) => {
    await page.goto('/generators');

    const characterCard = page.locator('a[href="/generators/character"]').first();
    await expect(characterCard).toBeVisible();
    await characterCard.click();

    await expect(page).toHaveURL('/generators/character');
  });
});
