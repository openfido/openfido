describe('app', () => {
  beforeAll(async () => {
    await page.setViewport({ width: 1024, height: 768 });
  })

  beforeEach(async () => {
    await page.goto('http://localhost:3001');
  });

  it('login admin@example.com', async () => {
    await page.type('input[aria-label="Email sign in input"]', 'admin@example.com', { delay: 100 });
    await page.type('input[aria-label="Password sign in input"]', '1234567890', { delay: 100 });
    await page.keyboard.press('Enter');

    await page.waitForTimeout(3000);

    await expect(page).toMatchElement('div[aria-label="Pipelines page title"]', {
      text: 'Pipelines',
    });
  });

  it('update user account admin@example.com', async () => {
    await page.click('a[aria-label="Settings menu link"]');
    await page.waitForTimeout(1000);

    await page.click('li[aria-label="Edit Profile settings item"]');
    await page.waitForTimeout(1000);

    await page.click('input[aria-label="First Name settings edit profile input"]', { clickCount: 3 });
    await page.keyboard.press('Backspace');
    await page.type('input[aria-label="First Name settings edit profile input"]', 'John', { delay: 100 });

    await page.click('input[aria-label="Last Name settings edit profile input"]', { clickCount: 3 });
    await page.keyboard.press('Backspace');
    await page.type('input[aria-label="Last Name settings edit profile input"]', 'Smith', { delay: 100 });

    // missing email change

    await page.keyboard.press('Enter');

    await page.waitForTimeout(3000);

    await page.click('button[aria-label="Return to Settings button"]');

    await expect(page).toMatchElement('div[aria-label="First name last name profile navigation"]', {
      text: 'John Smith',
    });
  });

  it('edit organization admin@example.com', async () => {
    await page.click('a[aria-label="Settings menu link"]');
    await page.waitForTimeout(1000);

    await page.click('li[aria-label="Edit Organization settings item"]');
    await page.waitForTimeout(1000);

    // edit the first organization
    await page.click('label[aria-label="Edit Organization edit label"]');

    await page.click('input[aria-label="Edit Organization edit input"]', { clickCount: 3 });
    await page.keyboard.press('Backspace');
    await page.type('input[aria-label="Edit Organization edit input"]', 'SLAC', { delay: 100 });

    await page.keyboard.press('Enter');
  });

  it('create organization admin@example.com', async () => {
    await page.click('a[aria-label="Settings menu link"]');
    await page.waitForTimeout(1000);

    await page.click('li[aria-label="Edit Organization settings item"]');
    await page.waitForTimeout(1000);

    // click on add organization
    await page.click('button[aria-label="Edit Organization add button"]');

    await page.click('input[aria-label="Edit Organization create input"]', { clickCount: 3 });
    await page.keyboard.press('Backspace');
    await page.type('input[aria-label="Edit Organization create input"]', 'Test Organization', { delay: 100 });

    await page.keyboard.press('Enter');
  });

  it('logout admin@example.com', async () => {
    await page.click('div[aria-label="App dropdown"]');
    await page.click('a[aria-label="Log Out link"]');
  });
});
