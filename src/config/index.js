const ENVIRONMENT_DEVELOPMENT = 'DEVELOPMENT';
const ENVIRONMENT_STAGING = 'STAGING';
const ENVIRONMENT_PRODUCTION = 'PRODUCTION';

const BASE_API_URL_APP_DEVELOPMENT = process.env.BASE_API_URL_APP_DEVELOPMENT || 'http://localhost:5000/v1';
const BASE_API_URL_AUTH_DEVELOPMENT = process.env.BASE_API_URL_AUTH_DEVELOPMENT || 'http://localhost:5002';

const BASE_API_URL_STAGING = process.env.BASE_API_URL_STAGING || 'https://api.staging.openfido.org';
const BASE_API_URL_PRODUCTION = process.env.BASE_API_URL_PRODUCTION || 'https://api.openfido.org';

const API_TOKEN = process.env.API_TOKEN || '846f2acb2f594f15a5e6dcdf69f85aa7';

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
else if (isStaging()) baseApiUrlAuth = BASE_API_URL_STAGING;
else if (isProduction()) baseApiUrlAuth = BASE_API_URL_PRODUCTION;

let baseApiUrlApp;
if (isDevelopment()) baseApiUrlApp = BASE_API_URL_APP_DEVELOPMENT;
else if (isStaging()) baseApiUrlApp = BASE_API_URL_STAGING;
else if (isProduction()) baseApiUrlApp = BASE_API_URL_PRODUCTION;

export default {
  api: {
    defaultTimeout: 10000,
    baseUrl: {
      auth: baseApiUrlAuth,
      app: baseApiUrlApp,
    },
    version: '',
    appToken: API_TOKEN,
  },
};
