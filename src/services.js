import ApiClient from 'util/api-client';

export const requestCreateUser = (organization_uuid, email, password, first_name, last_name) => (
  ApiClient.post('/users/create', {
    organization_uuid,
    email,
    password,
    first_name,
    last_name,
  })
);

export const requestLoginUser = (email, password) => ApiClient.post('/users/auth', {
  email,
  password,
});

export const requestRefreshJWT = () => ApiClient.post('/users/auth/refresh');

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

export const requestUserProfile = (user_uuid) => ApiClient.get(`/users/${user_uuid}/profile`);

export const requestOrganizationMembers = (organization_uuid) => (
  ApiClient.get(`/organizations/${organization_uuid}/members`)
);

export const requestRemoveOrganizationMember = (organization_uuid, user_uuid) => (
  ApiClient.delete(`/organizations/${organization_uuid}/members/${user_uuid}`)
);

export const requestChangeOrganizationMemberRole = (organization_uuid, user_uuid, role) => (
  ApiClient.post(`/organizations/${organization_uuid}/members/${user_uuid}/role`, { role })
);

export const requestInviteOrganizationMember = (organization_uuid, email) => (
  ApiClient.post(`/organizations/${organization_uuid}/invitations`, { email })
);

export const requestAcceptOrganizationInvitation = (organization_uuid, invitation_token) => (
  ApiClient.post(`/organizations/${organization_uuid}/invitations`, { invitation_token })
);
