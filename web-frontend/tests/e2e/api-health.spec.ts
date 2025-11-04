import { test, expect } from '@playwright/test';

test.describe('Backend API Health', () => {
  test('should have healthy backend on localhost:8001', async ({ request }) => {
    const response = await request.get('http://localhost:8001/health');
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data.status).toBe('healthy');
  });

  test('should return generator status with 17 generators', async ({ request }) => {
    const response = await request.get('http://localhost:8001/api/v1/generate/status');
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data.total_generators).toBe(17);
    expect(data.implemented).toBe(17);
    expect(data.generators).toHaveLength(17);
  });

  test('should generate character via API', async ({ request }) => {
    const response = await request.post('http://localhost:8001/api/v1/generate/character', {
      data: {
        name: 'E2E Test Mouse',
        gender: 'male',
      },
    });

    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data.name).toBe('E2E Test Mouse');
    expect(data).toHaveProperty('strength');
    expect(data).toHaveProperty('dexterity');
    expect(data).toHaveProperty('willpower');
  });

  test('should generate NPC via API', async ({ request }) => {
    const response = await request.post('http://localhost:8001/api/v1/generate/npc', {
      data: {},
    });

    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('name');
    expect(data).toHaveProperty('social_status');
    expect(data).toHaveProperty('appearance');
  });

  test('should generate weather via API', async ({ request }) => {
    const response = await request.post('http://localhost:8001/api/v1/generate/weather', {
      data: {
        season: 'winter',
        with_event: true,
      },
    });

    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data.season).toBe('winter');
    expect(data).toHaveProperty('weather');
    expect(data).toHaveProperty('event');
  });
});
