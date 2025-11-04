import { test, expect } from '@playwright/test';

test.describe('Weather Generator', () => {
  test('should load weather generator page', async ({ page }) => {
    await page.goto('/generators/weather');
    await expect(page.locator('h1')).toContainText('Weather Generator');
  });

  test('should have season selector', async ({ page }) => {
    await page.goto('/generators/weather');

    await expect(page.getByLabel(/Roční období/i)).toBeVisible();
    await expect(page.getByLabel(/Zahrnout sezónní událost/i)).toBeVisible();
  });

  test('should generate weather for spring', async ({ page }) => {
    await page.goto('/generators/weather');

    // Select spring (default)
    await page.getByRole('button', { name: /Generovat/i }).click();

    // Wait for result
    await page.waitForTimeout(2000);

    // Check season is displayed
    await expect(page.getByText(/Jaro/i)).toBeVisible();
  });

  test('should generate weather for winter', async ({ page }) => {
    await page.goto('/generators/weather');

    // Select winter
    await page.getByLabel(/Roční období/i).click();
    await page.getByRole('option', { name: /Zima/i }).click();

    await page.getByRole('button', { name: /Generovat/i }).click();
    await page.waitForTimeout(2000);

    await expect(page.getByText(/Zima/i)).toBeVisible();
  });

  test('should include event when checkbox is checked', async ({ page }) => {
    await page.goto('/generators/weather');

    // Check event checkbox
    await page.getByLabel(/Zahrnout sezónní událost/i).check();

    await page.getByRole('button', { name: /Generovat/i }).click();
    await page.waitForTimeout(2000);

    // Event section should be visible
    await expect(page.getByText(/SEZÓNNÍ UDÁLOST/i)).toBeVisible();
  });

  test('should display season info panel', async ({ page }) => {
    await page.goto('/generators/weather');

    await expect(page.getByText(/Info o ročních obdobích/i)).toBeVisible();
    await expect(page.getByText(/Přívalové deště/i)).toBeVisible();
    await expect(page.getByText(/Úmorné vedro/i)).toBeVisible();
  });
});
