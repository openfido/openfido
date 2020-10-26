const ENVIRONMENT_DEVELOPMENT = 'DEVELOPMENT';
const ENVIRONMENT_STAGING = 'STAGING';
const ENVIRONMENT_PRODUCTION = 'PRODUCTION';

const BASE_API_URL_AUTH_DEVELOPMENT = 'http://localhost:5002';
const BASE_API_URL_AUTH_STAGING = 'http://openfido-dev-auth-alb-665516109.us-east-1.elb.amazonaws.com';
const BASE_API_URL_AUTH_PRODUCTION = 'http://localhost:5002';

const BASE_API_URL_APP_DEVELOPMENT = 'http://localhost:5000/v1';
const BASE_API_URL_APP_STAGING = 'http://openfido-dev-app-alb-1500931865.us-east-1.elb.amazonaws.com/v1';
const BASE_API_URL_APP_PRODUCTION = 'http://localhost:5000/v1';

const API_TOKEN_DEVELOPMENT = process.env.API_TOKEN || '0e60a9e9fa794e6eb6849a4e73a21fa6';
const API_TOKEN_STAGING = process.env.API_TOKEN || '0e60a9e9fa794e6eb6849a4e73a21fa6';
const API_TOKEN_PRODUCTION = process.env.API_TOKEN || '0e60a9e9fa794e6eb6849a4e73a21fa6';

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

console.log('*****');
console.log(baseApiUrlApp);
console.log(baseApiUrlAuth);
console.log('*****');

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
