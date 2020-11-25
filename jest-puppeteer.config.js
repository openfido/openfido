module.exports = {
  server: {
    command: 'PORT=3001 npm start',
    port: 3001,
    launchTimeout: 120000,
    waitOnScheme: {
      delay: 25000,
    },
    debug: true,
  },
  launch: {
    dumpio: false,
    headless: false,
    args: ['--window-size=1920,1080'],
  },
  browser: 'chromium',
  browserContext: 'default',
};
