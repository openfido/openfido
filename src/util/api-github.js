// This file is meant to consolidate all utility function calls required to interact with the Github API

const axios = require('axios');

/// // END OF IMPORTS /////

// api scrape within openfido for all pipeline repositories
const potentialPipelines = `https://api.github.com/search/repositories?q=${encodeURIComponent('org:openfido Pipeline status in:readme')}`;

const gitApi = {

  getPotentialPipelines: async () => {
    const response = await axios.get(potentialPipelines, { timeout: 1500 });
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
    return response.data;
  },

};

module.exports = gitApi;
