import { test, expect } from '@playwright/test';

test.describe('Character Generator', () => {
  test('should load character generator page', async ({ page }) => {
    await page.goto('/generators/character');
    await expect(page.locator('h1')).toContainText('Character Generator');
  });

  test('should have form inputs', async ({ page }) => {
    await page.goto('/generators/character');

    await expect(page.getByLabel(/Jméno/i)).toBeVisible();
    await expect(page.getByLabel(/Pohlaví/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /Generovat/i })).toBeVisible();
  });

  test('should generate character with custom name', async ({ page }) => {
    await page.goto('/generators/character');

    // Fill form
    await page.getByLabel(/Jméno/i).fill('Testovací Myš');

    // Click generate
    await page.getByRole('button', { name: /Generovat/i }).click();

    // Wait for result
    await expect(page.locator('text=Testovací Myš')).toBeVisible({ timeout: 10000 });

    // Check stats are displayed
    await expect(page.getByText(/Síla/i)).toBeVisible();
    await expect(page.getByText(/Mrštnost/i)).toBeVisible();
    await expect(page.getByText(/Vůle/i)).toBeVisible();
  });

  test('should display inventory', async ({ page }) => {
    await page.goto('/generators/character');

    await page.getByRole('button', { name: /Generovat/i }).click();

    // Wait for character to load
    await page.waitForTimeout(2000);

    // Check inventory section is visible
    await expect(page.getByText(/Inventář/i)).toBeVisible();
  });

  test('should have Copy JSON button after generation', async ({ page }) => {
    await page.goto('/generators/character');

    await page.getByRole('button', { name: /Generovat/i }).click();
    await page.waitForTimeout(2000);

    await expect(page.getByRole('button', { name: /Copy JSON/i })).toBeVisible();
  });

  test('should reset form', async ({ page }) => {
    await page.goto('/generators/character');

    await page.getByLabel(/Jméno/i).fill('Test');
    await page.getByRole('button', { name: /Generovat/i }).click();
    await page.waitForTimeout(2000);

    // Click reset
    await page.getByRole('button', { name: /Reset/i }).click();

    // Name input should be empty
    await expect(page.getByLabel(/Jméno/i)).toHaveValue('');
  });
});
