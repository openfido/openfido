import axios from 'axios';
import config from 'config';
import Auth from 'util/auth';

///// END OF IMPORTS /////

// Create the .env file in the repo's root to store the Github APP secret so it does not get exposed on github.
// Create your own Github Oauth app for testing/using your own secret. Replace with Org Oauth App for deployment.

const GHUB_TOKEN_DEVELOPMENT = process.env.DEV_GAPP_TOKEN || 'UPDATE ENV';
const GHUB_TOKEN_STAGING = process.env.GHUB_API_TOKEN || 'UPDATE ENV';
const GHUB_TOKEN_PRODUCTION = process.env.GHUB_API_TOKEN || 'UPDATE ENV';

const oauth = require('axios-oauth-client');
const getAuthorizationCode = oauth.client(axios.create(), {
  url: 'https://oauth.com/2.0/token',
  grant_type: 'authorization_code',
  client_id: 'foo',
  client_secret: 'bar',
  redirect_uri: '...',
  code: '...',
  scope: 'baz',
});

const auth = await getAuthorizationCode(); // => { "access_token": "...", "expires_in": 900, ... }
