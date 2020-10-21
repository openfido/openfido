import axios from 'axios';
import config from 'config';
import Auth from 'util/auth';

export default class ApiClient {
  static get(url, service, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, auth, service).get(url);
  }

  static post(url, data = {}, service, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, auth, service).post(url, data);
  }

  static postForm(url, formFields, service, auth = true, timeout = config.api.defaultTimeout) {
    const data = new window.FormData();
    Object.keys(formFields).forEach((prop) => {
      data.set(prop, formFields[prop]);
    });

    return this.getInstance(timeout, auth, service, 'multipart/form-data').post(url, data);
  }

  static put(url, data = {}, service, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, auth, service).put(url, data);
  }

  static delete(url, service, auth = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, auth, service).delete(url);
  }

  static getInstance(
    timeout = config.api.defaultTimeout,
    auth = false,
    service,
    contentType = 'application/json',
    token = Auth.getUserToken(),
  ) {
    const headers = {
      'Content-Type': contentType,
    };

    if (auth && token !== null) {
      headers.Authorization = `Bearer ${token}`;
    }

    return axios.create({
      baseURL: `${service in config.api.baseUrl ? config.api.baseUrl[service] : config.api.baseUrl.app}${config.api.version}`,
      timeout,
      headers,
    });
  }
}
