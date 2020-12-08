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

  it('create pipeline Test Pipeline', async () => {
    await page.click('a[aria-label="Pipelines menu link"]');

    await page.click('button[aria-label="Add Pipeline button"]', 'admin@example.com', { delay: 100 });

    await page.type('input[aria-label="Pipeline Name input"]', 'Test Pipeline', { delay: 100 });
    await page.type('textarea[aria-label="Pipeline Description textarea"]', 'description', { delay: 100 });
    await page.type('input[aria-label="Pipeline DockerHub Repository input"]', 'python', { delay: 100 });
    await page.type('input[aria-label="Pipeline Repository input"]', 'https://github.com/PresencePG/presence-pipeline-example', { delay: 100 });
    await page.type('input[aria-label="Pipeline Repository Branch input"]', 'master', { delay: 100 });
    await page.click('input[aria-label="Pipeline Repository Script input"]', { clickCount: 3 });
    await page.keyboard.press('Backspace');
    await page.type('input[aria-label="Pipeline Repository Script input"]', 'openfido.sh', { delay: 100 });

    await page.keyboard.press('Enter');

    await page.waitForTimeout(3000);

    await page.click('a[aria-label="Pipelines menu link"]');

    await expect(page).toMatchElement('span[aria-label="Pipeline Item name"]', {
      text: 'Test Pipeline',
    });
  });

  it('start pipeline Test pipeline', async () => {
    await page.click('a[aria-label="Pipelines menu link"]');

    await page.waitForTimeout(3000);

    await page.click('button[aria-label="Test Pipeline View Runs button"]');

    await page.click('button[aria-label="Start a run button"]');

    await page.click('button[aria-label="Start Run button"]');

    await page.waitForTimeout(3000);

    await expect(page).toMatchElement('mark[aria-label="Run Item status mark"]', {
      text: 'In Progress',
    });
  });

  it('logout admin@example.com', async () => {
    await page.click('div[aria-label="App dropdown"]');
    await page.click('a[aria-label="Log Out link"]');
  });
});
