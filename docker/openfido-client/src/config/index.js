const ENVIRONMENT_DEVELOPMENT = 'DEVELOPMENT';
const ENVIRONMENT_STAGING = 'STAGING';
const ENVIRONMENT_PRODUCTION = 'PRODUCTION';

const BASE_API_URL_AUTH_DEVELOPMENT = 'http://localhost:6002';
const BASE_API_URL_AUTH_STAGING = 'https://auth-staging.openfido.org';
const BASE_API_URL_AUTH_PRODUCTION = 'https://auth.openfido.org';

const BASE_API_URL_APP_DEVELOPMENT = 'http://localhost:6003/v1';
const BASE_API_URL_APP_STAGING = 'https://api-staging.openfido.org/v1';
const BASE_API_URL_APP_PRODUCTION = 'https://api.openfido.org/v1';

const API_TOKEN_DEVELOPMENT = process.env.REACT_APP_API_TOKEN;
const API_TOKEN_STAGING = process.env.API_TOKEN || '1ad2a5f2e82d402f81a7781721a92e67' ;
const API_TOKEN_PRODUCTION = process.env.API_TOKEN || '250b7248ca9b4986825714f4d344f9a4';

const parseEnvironment = () => {
  if (window.location.hostname.includes('localhost')) return ENVIRONMENT_DEVELOPMENT;
  if (window.location.hostname.includes('staging')) return ENVIRONMENT_STAGING;
  return ENVIRONMENT_PRODUCTION;
};

export const ENVIRONMENT = parseEnvironment();
export const isDevelopment = () => (ENVIRONMENT === ENVIRONMENT_DEVELOPMENT);
export const isStaging = () => (ENVIRONMENT === ENVIRONMENT_STAGING);
export const isProduction = () => (ENVIRONMENT === ENVIRONMENT_PRODUCTION);

let baseApiUrlAuth;
if (isDevelopment()) baseApiUrlAuth = BASE_API_URL_AUTH_DEVELOPMENT;
else if (isStaging()) baseApiUrlAuth = BASE_API_URL_AUTH_STAGING;
else if (isProduction()) baseApiUrlAuth = BASE_API_URL_AUTH_PRODUCTION;

let baseApiUrlApp;
if (isDevelopment()) baseApiUrlApp = BASE_API_URL_APP_DEVELOPMENT;
else if (isStaging()) baseApiUrlApp = BASE_API_URL_APP_STAGING;
else if (isProduction()) baseApiUrlApp = BASE_API_URL_APP_PRODUCTION;

let apiToken;
if (isDevelopment()) apiToken = API_TOKEN_DEVELOPMENT;
else if (isStaging()) apiToken = API_TOKEN_STAGING;
else if (isProduction()) apiToken = API_TOKEN_PRODUCTION;

export default {
  api: {
    defaultTimeout: 60000,
    baseUrl: {
      auth: baseApiUrlAuth,
      app: baseApiUrlApp,
    },
    version: '',
    appToken: apiToken,
  },
};
