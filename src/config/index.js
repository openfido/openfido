const ENVIRONMENT_DEVELOPMENT = 'DEVELOPMENT';
const ENVIRONMENT_STAGING = 'STAGING';
const ENVIRONMENT_PRODUCTION = 'PRODUCTION';

const BASE_API_URL_AUTH_DEVELOPMENT = 'http://localhost:6002';
const BASE_API_URL_AUTH_STAGING = 'http://openfido-dev-auth-alb-433407301.us-east-1.elb.amazonaws.com';
const BASE_API_URL_AUTH_PRODUCTION = 'http://localhost:6002';

const BASE_API_URL_APP_DEVELOPMENT = 'http://localhost:8080/v1';
const BASE_API_URL_APP_STAGING = 'http://openfido-dev-app-alb-654410805.us-east-1.elb.amazonaws.com/v1';
const BASE_API_URL_APP_PRODUCTION = 'http://localhost:8080/v1';

const API_TOKEN_DEVELOPMENT = process.env.API_TOKEN || 'e7d79ec348b540b78f03a59d0956bacf';
const API_TOKEN_STAGING = process.env.API_TOKEN || '2c873e166d1e40439de6f811104134e7';
const API_TOKEN_PRODUCTION = process.env.API_TOKEN || '2c873e166d1e40439de6f811104134e7';

const parseEnvironment = () => {
  if (window.location.hostname.includes('localhost')) return ENVIRONMENT_DEVELOPMENT;
  if (window.location.hostname.includes('cloudfront')) return ENVIRONMENT_STAGING;
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
    defaultTimeout: 10000,
    baseUrl: {
      auth: baseApiUrlAuth,
      app: baseApiUrlApp,
    },
    version: '',
    appToken: apiToken,
  },
};
