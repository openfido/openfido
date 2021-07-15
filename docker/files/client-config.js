import { API_TOKEN } from './reactclient';

export default {
  api: {
    defaultTimeout: 60000,
    baseUrl: {
      auth: 'http://localhost:5001',
      app: 'http://localhost:5003/v1',
    },
    version: '',
    appToken: API_TOKEN,
  },
};
