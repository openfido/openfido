import ApiClient from 'util/api-client';

export const requestCreateUser = (email, password, invitation_token) => (
  ApiClient.post('/users', {
    email,
    password,
    invitation_token,
    first_name: 'User',
    last_name: 'Example',
  })
);

export const requestLoginUser = (email, password) => ApiClient.post('/users/auth', {
  email,
  password,
});

export const requestRefreshJWT = () => ApiClient.post('/users/auth/refresh');

export const requestPasswordReset = (email) => ApiClient.post('/users/request_password_reset', {
  email,
});

export const requestUpdatePassword = (reset_token, password) => (
  ApiClient.put('/users/reset_password', {
    reset_token,
    password,
  })
);

export const requestChangePassword = (old_password, new_password) => (
  ApiClient.put('/users/password', {
    old_password,
    new_password,
  })
);

export const requestUserProfile = (user_uuid) => ApiClient.get(`/users/${user_uuid}/profile`);

export const requestUserOrganizations = (user_uuid) => ApiClient.get(`/users/${user_uuid}/organizations`);

export const requestUpdateUserProfile = (user_uuid, email, first_name, last_name) => (
  ApiClient.put(`/users/${user_uuid}/profile`, {
    email,
    first_name,
    last_name,
  })
);

export const requestUserAvatar = (user_uuid) => (
  ApiClient.get(`/users/${user_uuid}/avatar`)
);

export const requestUpdateUserAvatar = (user_uuid, image_content) => (
  ApiClient.put(`/users/${user_uuid}/avatar`, image_content)
);

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

export const requestAcceptOrganizationInvitation = (invitation_token) => (
  ApiClient.post('/organizations/invitations/accept', { invitation_token })
);

export const requestCancelOrganizationInvitation = (invitation_uuid) => (
  ApiClient.post('/organizations/invitations/cancel', { invitation_uuid })
);

export const requestOrganizationInvitations = (organization_uuid) => (
  ApiClient.get(`/organizations/${organization_uuid}/invitations`)
);

export const requestCreateOrganization = (organization_name) => (
  ApiClient.post('/organizations', { name: organization_name })
);

export const requestUpdateOrganization = (organization_uuid, organization_name) => (
  ApiClient.put(`/organizations/${organization_uuid}/profile`, { name: organization_name })
);

export const requestDeleteOrganization = (organization_uuid) => (
  ApiClient.delete(`/organizations/${organization_uuid}`)
);
