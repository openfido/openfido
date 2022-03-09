// This file is meant to consolidate all utility function calls required to interact with the Github API

const axios = require('axios');
const oauth = require('axios-oauth-client');

/// // END OF IMPORTS /////

// Create the .env file in the repo's root to store the Github APP secret so it does not get exposed on github.
// Create your own Github Oauth app for testing/using your own secret. Replace with Org Oauth App for deployment.

const GHUB_TOKEN_DEVELOPMENT = process.env.DEV_GAPP_SECRET || 'UPDATE ENV';
const GHUB_TOKEN_STAGING = process.env.GHUB_API_SECRET || 'UPDATE ENV';
const GHUB_TOKEN_PRODUCTION = process.env.GHUB_API_SECRET || 'UPDATE ENV';

const GHUB_CLIENT_ID = process.env.GHUB_CLIENT_ID || 'UPDATE ENV';

// api scrape within openfido for all pipeline repositories
const potentialPipelines = `https://api.github.com/search/repositories?q=${encodeURIComponent('org:openfido pipeline settings in:readme')}`;

const gitApi = {

  getPotentialPipelines: async () => {
    const response = await axios.get(potentialPipelines, { timeout: 1500 });
    console.log(response.data);
    return response.data;
  },

  // accept header application/vnd.github.VERSION.raw is REQUIRED to decrypt file contents
  getManifest: async (url) => {
    const temp = `${url}/contents/manifest.json`;
    const response = await axios.get(temp, {
      headers: {
        accept: 'application/vnd.github.VERSION.raw',
      },
    });
    console.log(response.data);
    return response.data.content;
  },

};

module.exports = gitApi;
