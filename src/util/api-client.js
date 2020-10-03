import axios from 'axios';
import config from 'config';
import Auth from 'util/auth';

export default class ApiClient {
  static get(url, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, auth).get(url);
  }

  static post(url, data = {}, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, auth).post(url, data);
  }

  static postForm(url, formFields) {
    const data = new window.FormData();
    Object.keys(formFields).forEach((prop) => {
      data.set(prop, formFields[prop]);
    });

    return this.getInstance(config.api.defaultTimeout, 'multipart/form-data').post(url, data);
  }

  static put(url, data = {}, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, auth).put(url, data);
  }

  static delete(url, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, auth).delete(url);
  }

  static getInstance(
    timeout = config.api.defaultTimeout,
    auth = false,
    token = Auth.getAuthToken(),
    contentType = 'application/json',
  ) {
    const headers = {
      'Content-Type': contentType,
    };

    if (auth && token !== null) {
      headers.Authorization = `Bearer ${token}`;
    }

    return axios.create({
      baseURL: `${config.api.baseUrl}${config.api.version}`,
      timeout,
      headers,
    });
  }
}
