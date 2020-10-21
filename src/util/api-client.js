import axios from 'axios';
import config from 'config';
import Auth from 'util/auth';

export default class ApiClient {
  static get(url, apiKey, useAuthKey = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey, useAuthKey).get(url);
  }

  static post(url, data = {}, apiKey, useAuthKey = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey, useAuthKey).post(url, data);
  }

  static postForm(url, formFields, apiKey, useAuthKey = true, timeout = config.api.defaultTimeout) {
    const data = new window.FormData();
    Object.keys(formFields).forEach((prop) => {
      data.set(prop, formFields[prop]);
    });

    return this.getInstance(timeout, apiKey, useAuthKey, 'multipart/form-data').post(url, data);
  }

  static put(url, data = {}, apiKey, useAuthKey = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey, useAuthKey).put(url, data);
  }

  static delete(url, apiKey, useAuthKey = true, timeout = config.api.defaultTimeout) {
    return this.getInstance(timeout, apiKey, useAuthKey).delete(url);
  }

  static getInstance(
    timeout = config.api.defaultTimeout,
    apiKey,
    useAuthKey = false,
    contentType = 'application/json',
    token = Auth.getUserToken(),
  ) {
    const headers = {
      'Content-Type': contentType,
    };

    if (apiKey) {
      headers['Workflow-API-Key'] = apiKey;
    }

    if (useAuthKey && token !== null) {
      headers.Authorization = `Bearer ${token}`;
    }

    return axios.create({
      timeout,
      headers,
    });
  }
}
