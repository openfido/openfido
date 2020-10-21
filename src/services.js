import ApiClient from 'util/api-client';

export const requestCreateUser = (email, first_name, last_name, password, invitation_token) => (
  ApiClient.post('/users', {
    email,
    first_name,
    last_name,
    password,
    invitation_token,
  }, 'auth')
);

export const requestLoginUser = (email, password) => ApiClient.post('/users/auth', {
  email,
  password,
}, 'auth');

export const requestRefreshJWT = () => ApiClient.post('/users/auth/refresh', {}, 'auth');

export const requestPasswordReset = (email) => ApiClient.post('/users/request_password_reset', {
  email,
}, 'auth');

export const requestUpdatePassword = (reset_token, password) => (
  ApiClient.put('/users/reset_password', {
    reset_token,
    password,
  }, 'auth')
);

export const requestChangePassword = (old_password, new_password) => (
  ApiClient.put('/users/password', {
    old_password,
    new_password,
  }, 'auth')
);

export const requestUserProfile = (user_uuid) => ApiClient.get(`/users/${user_uuid}/profile`, 'auth');

export const requestUserOrganizations = (user_uuid) => ApiClient.get(`/users/${user_uuid}/organizations`, 'auth');

export const requestUpdateUserProfile = (user_uuid, email, first_name, last_name) => (
  ApiClient.put(`/users/${user_uuid}/profile`, {
    email,
    first_name,
    last_name,
  }, 'auth')
);

export const requestUserAvatar = (user_uuid) => (
  ApiClient.get(`/users/${user_uuid}/avatar`, 'auth')
);

export const requestUpdateUserAvatar = (user_uuid, image_content) => (
  ApiClient.put(`/users/${user_uuid}/avatar`, image_content, 'auth')
);

export const requestOrganizationMembers = (organization_uuid) => (
  ApiClient.get(`/organizations/${organization_uuid}/members`, 'auth')
);

export const requestRemoveOrganizationMember = (organization_uuid, user_uuid) => (
  ApiClient.delete(`/organizations/${organization_uuid}/members/${user_uuid}`, 'auth')
);

export const requestChangeOrganizationMemberRole = (organization_uuid, user_uuid, role) => (
  ApiClient.put(`/organizations/${organization_uuid}/members/${user_uuid}/role`, { role }, 'auth')
);

export const requestInviteOrganizationMember = (organization_uuid, email) => (
  ApiClient.post(`/organizations/${organization_uuid}/invitations`, { email }, 'auth')
);

export const requestAcceptOrganizationInvitation = (invitation_token) => (
  ApiClient.post('/organizations/invitations/accept', { invitation_token }, 'auth')
);

export const requestCancelOrganizationInvitation = (invitation_uuid) => (
  ApiClient.post('/organizations/invitations/cancel', { invitation_uuid }, 'auth')
);

export const requestOrganizationInvitations = (organization_uuid) => (
  ApiClient.get(`/organizations/${organization_uuid}/invitations`, 'auth')
);

export const requestCreateOrganization = (organization_name) => (
  ApiClient.post('/organizations', { name: organization_name }, 'auth')
);

export const requestUpdateOrganization = (organization_uuid, organization_name) => (
  ApiClient.put(`/organizations/${organization_uuid}/profile`, { name: organization_name }, 'auth')
);

export const requestDeleteOrganization = (organization_uuid) => (
  ApiClient.delete(`/organizations/${organization_uuid}`, 'app')
);
