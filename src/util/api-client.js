import axios from 'axios';
import config from 'config';
import Auth from './auth';

export default class ApiClient {
  static get(url, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout).get(url);
  }

  static post(url, data = {}, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout).post(url, data);
  }

  static postForm(url, formFields) {
    const data = new window.FormData();
    // eslint-disable-next-line guard-for-in,no-restricted-syntax
    for (const prop in formFields) {
      data.set(prop, formFields[prop]);
    }

    return this.getInstance(config.api.defaultTimeout, 'multipart/form-data').post(url, data);
  }

  static put(url, data = {}, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout).put(url, data);
  }

  static delete(url, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout).delete(url);
  }

  static getInstance(
    timeout = config.api.defaultTimeout,
    contentType = 'application/json',
  ) {
    const headers = {
      'Content-Type': contentType,
    };

    if (Auth.isUserLoggedIn()) {
      headers.Authorization = `Bearer ${Auth.getAuthToken()}`;
    }

    const apiInstance = axios.create({
      baseURL: `${config.api.baseUrl}`,
      timeout,
      headers,
    });

    return apiInstance;
  }
}
