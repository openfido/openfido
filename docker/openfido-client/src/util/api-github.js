// This file is meant to consolidate all utility function calls required to interact with the Github API

const axios = require('axios');

/// // END OF IMPORTS /////

// api scrape within openfido for all pipeline repositories
const potentialPipelines = `https://api.github.com/search/repositories?q=${encodeURIComponent('org:openfido "Pipeline status" in:readme')}`;

const gitApi = {

  // list for dropdown of all repositories that can generate a pipeline, cleaned of excess data
  getPotentialPipelines: async () => {
    const response = await axios.get(potentialPipelines, { timeout: 1500 });
    const data = response.data.items;
    const cleanData = data.map((repo) => {
      const reducedData = {};
      reducedData.full_name = repo.name;
      reducedData.url = repo.url;
      reducedData.id = repo.id;
      reducedData.description = repo.description;
      return reducedData;
    });
    return cleanData;
  },

  // data from selected pipeline to pre-fill pipeline form, expecting a url string
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

export default gitApi;
