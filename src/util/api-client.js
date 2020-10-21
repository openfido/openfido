import axios from 'axios';
import config from 'config';
import Auth from 'util/auth';

export default class ApiClient {
  static get(url, apiKey, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey, auth).get(url);
  }

  static post(url, data = {}, apiKey, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey, auth).post(url, data);
  }

  static postForm(url, formFields, apiKey, auth = true, timeout = config.api.defaultTimeout) {
    const data = new window.FormData();
    Object.keys(formFields).forEach((prop) => {
      data.set(prop, formFields[prop]);
    });

    return this.getInstance(timeout, apiKey, auth, 'multipart/form-data').post(url, data);
  }

  static put(url, data = {}, apiKey, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey, auth).put(url, data);
  }

  static delete(url, apiKey, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey, auth).delete(url);
  }

  static getInstance(
    timeout = config.api.defaultTimeout,
    apiKey,
    auth = false,
    contentType = 'application/json',
    token = Auth.getUserToken(),
  ) {
    const headers = {
      'Content-Type': contentType,
    };

    if (apiKey) {
      headers['Workflow-API-Key'] = apiKey;
    }

    if (auth && token !== null) {
      headers.Authorization = `Bearer ${token}`;
    }

    return axios.create({
      timeout,
      headers,
    });
  }
}
