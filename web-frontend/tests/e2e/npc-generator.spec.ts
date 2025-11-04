import { test, expect } from '@playwright/test';

test.describe('NPC Generator', () => {
  test('should load NPC generator page', async ({ page }) => {
    await page.goto('/generators/npc');
    await expect(page.locator('h1')).toContainText('NPC Generator');
  });

  test('should generate NPC successfully', async ({ page }) => {
    await page.goto('/generators/npc');

    await page.getByRole('button', { name: /Generovat/i }).click();

    // Wait for result
    await page.waitForTimeout(2000);

    // Check NPC fields are displayed
    await expect(page.getByText(/Rodné znamení/i)).toBeVisible();
    await expect(page.getByText(/Vzhled/i)).toBeVisible();
    await expect(page.getByText(/Zvláštnost/i)).toBeVisible();
    await expect(page.getByText(/Po čem touží/i)).toBeVisible();
  });

  test('should generate NPC with custom name', async ({ page }) => {
    await page.goto('/generators/npc');

    await page.getByLabel(/Jméno/i).fill('Strážný Karel');
    await page.getByRole('button', { name: /Generovat/i }).click();

    await expect(page.locator('text=Strážný Karel')).toBeVisible({ timeout: 10000 });
  });

  test('should display reaction info', async ({ page }) => {
    await page.goto('/generators/npc');

    await page.getByRole('button', { name: /Generovat/i }).click();
    await page.waitForTimeout(2000);

    await expect(page.getByText(/Reakce při setkání/i)).toBeVisible();
  });

  test('should have copy and save buttons', async ({ page }) => {
    await page.goto('/generators/npc');

    await page.getByRole('button', { name: /Generovat/i }).click();
    await page.waitForTimeout(2000);

    await expect(page.getByRole('button', { name: /Copy JSON/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /Save/i })).toBeVisible();
  });
});
