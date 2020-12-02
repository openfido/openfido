import axios from 'axios';
import config from 'config';
import Auth from 'util/auth';

export default class ApiClient {
  static get(url, apiKey, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey).get(url);
  }

  static post(url, data = {}, apiKey, contentType = 'application/json', timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey, contentType).post(url, data);
  }

  static postForm(url, data, apiKey, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey, 'multipart/form-data').post(url, data);
  }

  static put(url, data = {}, apiKey, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey).put(url, data);
  }

  static delete(url, apiKey, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey).delete(url);
  }

  static getInstance(
    timeout = config.api.defaultTimeout,
    apiKey,
    contentType = 'application/json',
    token = Auth.getUserToken(),
  ) {
    const headers = {
      'Content-Type': contentType,
    };

    if (apiKey) {
      headers['Workflow-API-Key'] = apiKey;
    }

    if (token !== null) {
      headers.Authorization = `Bearer ${token}`;
    }

    return axios.create({
      timeout,
      headers,
    });
  }
}
