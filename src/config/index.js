const ENVIRONMENT_DEVELOPMENT = 'DEVELOPMENT';
const ENVIRONMENT_STAGING = 'STAGING';
const ENVIRONMENT_PRODUCTION = 'PRODUCTION';

const BASE_URL_DEVELOPMENT = 'http://localhost:5000';
const BASE_URL_STAGING = 'https://staging.openfido.org';
const BASE_URL_PRODUCTION = 'https://www.openfido.org';

const parseEnvironment = () => {
  if (window.location.hostname.includes('localhost')) return ENVIRONMENT_DEVELOPMENT;
  if (window.location.hostname.includes('staging')) return ENVIRONMENT_STAGING;
  return ENVIRONMENT_PRODUCTION;
};

export const ENVIRONMENT = parseEnvironment();
export const isDevelopment = () => (ENVIRONMENT === ENVIRONMENT_DEVELOPMENT);
export const isStaging = () => (ENVIRONMENT === ENVIRONMENT_STAGING);
export const isProduction = () => (ENVIRONMENT === ENVIRONMENT_PRODUCTION);

let baseUrl;
if (isDevelopment()) baseUrl = BASE_URL_DEVELOPMENT;
else if (isStaging()) baseUrl = BASE_URL_STAGING;
else if (isProduction()) baseUrl = BASE_URL_PRODUCTION;

export default {
  api: {
    defaultTimeout: 10000,
    baseUrl,
  },
};
