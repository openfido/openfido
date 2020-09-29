import ApiClient from 'util/api-client';

export const requestLoginUser = (email, password) => ApiClient.post('/users/auth', {
  email,
  password,
});

export const requestRefreshJWT = (token) => ApiClient.post('/users/auth/refresh', {}, token);
