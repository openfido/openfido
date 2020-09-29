import axios from 'axios';
import config from 'config';

export default class ApiClient {
  static get(url, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout).get(url);
  }

  static post(url, data = {}, token = null, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, token).post(url, data);
  }

  static postForm(url, formFields) {
    const data = new window.FormData();
    Object.keys(formFields).forEach((prop) => {
      data.set(prop, formFields[prop]);
    });

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
    token = null,
    contentType = 'application/json',
  ) {
    const headers = {
      'Content-Type': contentType,
    };

    if (token !== null) {
      headers.Authorization = `Bearer ${token}`;
    }

    return axios.create({
      baseURL: `${config.api.baseUrl}${config.api.version}`,
      timeout,
      headers,
    });
  }
}
