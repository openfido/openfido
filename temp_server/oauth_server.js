require('dotenv').config();
const axios = require('axios');
const express = require('express');
const path = require('path');

const app = express();
const port = 3005;

app.get('/', (req, res) => {
  res.send('This page isn\'t for humans!');
});

app.get('/auth', (req, res) => {
  res.redirect(
    `https://github.com/login/oauth/authorize?client_id=${process.env.GHUB_CLIENT_ID}`,
  );
});

app.get('/oauth-callback', ({ query: { code } }, res) => {
  const body = {
    client_id: process.env.GHUB_CLIENT_ID,
    client_secret: process.env.DEV_GAPP_SECRET,
    code,
  };
  const opts = { headers: { accept: 'application/json' } };
  axios
    .post('https://github.com/login/oauth/access_token', body, opts)
    .then((_res) => _res.data.access_token)
    .then((token) => {
      // eslint-disable-next-line no-console
      console.log('My token:', token);

      res.redirect(`/?token=${token}`);
    })
    .catch((err) => res.status(500).json({ err: err.message }));
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
