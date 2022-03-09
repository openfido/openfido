// This file is meant to consolidate all utility function calls required to interact with the Github API

const axios = require('axios');
const oauth = require('axios-oauth-client');

///// END OF IMPORTS /////

// Create the .env file in the repo's root to store the Github APP secret so it does not get exposed on github.
// Create your own Github Oauth app for testing/using your own secret. Replace with Org Oauth App for deployment.

const GHUB_TOKEN_DEVELOPMENT = process.env.DEV_GAPP_SECRET || 'UPDATE ENV';
const GHUB_TOKEN_STAGING = process.env.GHUB_API_SECRET || 'UPDATE ENV';
const GHUB_TOKEN_PRODUCTION = process.env.GHUB_API_SECRET || 'UPDATE ENV';

const GHUB_CLIENT_ID = process.env.GHUB_CLIENT_ID || 'UPDATE ENV';

const gitApi = {

    getAuthorizationCode: oauth.client(axios.create(), {
        url: 'https://github.com/login/oauth/authorize?',
        type: 'user_agent',
        client_id: GHUB_CLIENT_ID,
        client_secret: GHUB_TOKEN_DEVELOPMENT,
        redirect_uri: 'https://localhost:3000/pipelines/Oauth2',
        code: '...'
      }),

      auth: await getAuthorizationCode(), // => { "access_token": "...", "expires_in": 900, ... }

      getMostFollowedUsers: async() => {
        const noOfFollowers = 35000;
        const perPage = 10;
        //ref: https://docs.GitHub.com/en/GitHub/searching-for-information-on-GitHub/searching-on-GitHub/searching-users
        const response = await GitHubClient.get(`search/users?q=followers:>${noOfFollowers}&per_page=${perPage}`, {timeout: 1500});
        return response.data.items;
      },

}


const auth = await getAuthorizationCode(); // => { "access_token": "...", "expires_in": 900, ... }

const GitHubClient = axios.create({
    baseURL: 'https://api.GitHub.com/',
    timeout: 1000,
    headers: {
      'Accept': 'application/vnd.GitHub.v3+json',
      //'Authorization': 'token <your-token-here> -- https://docs.GitHub.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token'
    }
  });
  
  
  async function getCounts(username) {
    const response = await GitHubClient.get(`users/${username}`);
    return {
      username,
      name: response.data.name,
      publicReposCount: response.data.public_repos,
      followersCount: response.data.followers
    };  
  }
  
  (async () => {
    try {
      const mostFollowedUsers = await getMostFollowedUsers();
      const popularUsernames = mostFollowedUsers.map(user => user.login);
      const popularUsersWithPublicRepoCount = await Promise.all(popularUsernames.map(getCounts));
      console.table(popularUsersWithPublicRepoCount);
  
      console.log(`======== Another view ========`);
      popularUsersWithPublicRepoCount.forEach((userWithPublicRepos) => {
        console.log(`${userWithPublicRepos.name} with username ${userWithPublicRepos.username} has ${userWithPublicRepos.publicReposCount} public repos and ${userWithPublicRepos.followersCount} followers on GitHub`);
      });
    } catch(error) {
      console.log(`Error calling GitHub API: ${error.message}`, error);
    }
  })();

  module.exports = gitApi; 