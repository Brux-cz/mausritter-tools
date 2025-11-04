import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should load successfully', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Mausritter Tools/);
  });

  test('should display main heading', async ({ page }) => {
    await page.goto('/');
    const heading = page.locator('h1');
    await expect(heading).toContainText('Mausritter Tools');
  });

  test('should display CTA buttons', async ({ page }) => {
    await page.goto('/');
    const startButton = page.getByRole('button', { name: /Start Free/i });
    const learnButton = page.getByRole('button', { name: /Learn More/i });

    await expect(startButton).toBeVisible();
    await expect(learnButton).toBeVisible();
  });

  test('should display feature boxes', async ({ page }) => {
    await page.goto('/');

    // Check for three feature boxes
    await expect(page.getByText('Generátory')).toBeVisible();
    await expect(page.getByText('Hexcrawl Manager')).toBeVisible();
    await expect(page.getByText('Character Sheets')).toBeVisible();
  });

  test('should display features list', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByText('17 generátorů')).toBeVisible();
    await expect(page.getByText('Campaign management')).toBeVisible();
    await expect(page.getByText('100% zdarma')).toBeVisible();
  });
});
