require('dotenv').config();
const axios = require('axios');
const express = require('express');
const path = require('path');
const gitApi = require('../src/util/api-github');

const app = express();
const port = 3005;

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', 'http://localhost:3000'); // update to match the domain you will make the request from
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

let gtoken;

app.get('/', (req, res) => {
  res.send('This page isn\'t for humans!');
});

app.get('/auth', (req, res) => {
  res.redirect(
    `https://github.com/login/oauth/authorize?client_id=${process.env.GHUB_CLIENT_ID}`,
  );
});

app.get('/pipelines/Oauth2', ({ query: { code } }, res) => {
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

      gtoken = token;

      res.redirect('http://localhost:3000/pipelines');
    })
    .catch((err) => res.status(500).json({ err: err.message }));
});

// current functional internal method to retrieve token and grant Oauth search priviledges, **needs security improvement**
app.get('/gtoken', (req, res) => {
  res.send(
    `${gtoken}`,
  );
});

// list for dropdown of all repositories that can generate a pipeline
app.get('/autogenPipelines', async (req, res) => {
  const data = await gitApi.getPotentialPipelines();
  console.log('hmmmmm1', data);
  res.send(data);
});

// data from selected pipeline to pre-fill pipeline form
app.get('/pipelineManifest', async (req, res) => {
  const data = await gitApi.getPotentialPipelines();
  console.log('hmmmmm1', data);
  res.send(data);
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
