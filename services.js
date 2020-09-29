import ApiClient from 'util/api-client';

export const requestPasswordReset = (email) => ApiClient.post('/users/auth/reset', {
  email,
});
``
export const requestUpdatePassword = (email, reset_token, password) => (
  ApiClient.put('/users/auth/update-password', {
    email,
    reset_token,
    password,
  })``
);
