import ApiClient from 'util/api-client';

export const requestLoginUser = (email, password) => ApiClient.post('/users/auth', {
  email,
  password,
});

export const requestRefreshJWT = (token) => ApiClient.post('/users/auth/refresh', {}, token);

export const requestPasswordReset = (email) => ApiClient.post('/users/auth/reset', {
  email,
});

export const requestUpdatePassword = (email, reset_token, password) => (
  ApiClient.put('/users/auth/update-password', {
    email,
    reset_token,
    password,
  })
);

export const requestUserProfile = (user_uuid, token) => ApiClient.get(`/users/${user_uuid}/profile`, token);

export const requestOrganizationMembers = (organization_uuid, token) => (
  ApiClient.get(`/organizations/${organization_uuid}/members`, token)
);
