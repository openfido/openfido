import ApiClient from 'util/api-client';
import config from 'config';

const { baseUrl, appToken } = config.api;

export const requestCreateUser = (email, first_name, last_name, password, invitation_token) => (
  ApiClient.post(`${baseUrl.auth}/users`, {
    email,
    first_name,
    last_name,
    password,
    invitation_token,
  })
);

export const requestLoginUser = (email, password) => ApiClient.post(`${baseUrl.auth}/users/auth`, {
  email,
  password,
});

export const requestRefreshJWT = () => ApiClient.post(`${baseUrl.auth}/users/auth/refresh`, {});

export const requestPasswordReset = (email) => ApiClient.post(`${baseUrl.auth}/users/request_password_reset`, {
  email,
});

export const requestUpdatePassword = (reset_token, password) => (
  ApiClient.put(`${baseUrl.auth}/users/reset_password`, {
    reset_token,
    password,
  })
);

export const requestChangePassword = (old_password, new_password) => (
  ApiClient.put(`${baseUrl.auth}/users/password`, {
    old_password,
    new_password,
  })
);

export const requestUserProfile = (user_uuid) => ApiClient.get(`${baseUrl.auth}/users/${user_uuid}/profile`);

export const requestUserOrganizations = (user_uuid) => ApiClient.get(`${baseUrl.auth}/users/${user_uuid}/organizations`);

export const requestUpdateUserProfile = (user_uuid, email, first_name, last_name) => (
  ApiClient.put(`${baseUrl.auth}/users/${user_uuid}/profile`, {
    email,
    first_name,
    last_name,
  })
);

export const requestUserAvatar = (user_uuid) => (
  ApiClient.get(`${baseUrl.auth}/users/${user_uuid}/avatar`)
);

export const requestUpdateUserAvatar = (user_uuid, image_content) => (
  ApiClient.put(`${baseUrl.auth}/users/${user_uuid}/avatar`, image_content)
);

export const requestOrganizationMembers = (organization_uuid) => (
  ApiClient.get(`${baseUrl.auth}/organizations/${organization_uuid}/members`)
);

export const requestRemoveOrganizationMember = (organization_uuid, user_uuid) => (
  ApiClient.delete(`${baseUrl.auth}/organizations/${organization_uuid}/members/${user_uuid}`)
);

export const requestChangeOrganizationMemberRole = (organization_uuid, user_uuid, role) => (
  ApiClient.put(`${baseUrl.auth}/organizations/${organization_uuid}/members/${user_uuid}/role`, { role })
);

export const requestInviteOrganizationMember = (organization_uuid, email) => (
  ApiClient.post(`${baseUrl.auth}/organizations/${organization_uuid}/invitations`, { email })
);

export const requestAcceptOrganizationInvitation = (invitation_token) => (
  ApiClient.post(`${baseUrl.auth}/organizations/invitations/accept`, { invitation_token })
);

export const requestCancelOrganizationInvitation = (invitation_uuid) => (
  ApiClient.post(`${baseUrl.auth}/organizations/invitations/cancel`, { invitation_uuid })
);

export const requestOrganizationInvitations = (organization_uuid) => (
  ApiClient.get(`${baseUrl.auth}/organizations/${organization_uuid}/invitations`)
);

export const requestCreateOrganization = (organization_name) => (
  ApiClient.post(`${baseUrl.auth}/organizations`, { name: organization_name })
);

export const requestUpdateOrganization = (organization_uuid, organization_name) => (
  ApiClient.put(`${baseUrl.auth}/organizations/${organization_uuid}/profile`, { name: organization_name })
);

export const requestDeleteOrganization = (organization_uuid) => (
  ApiClient.delete(`${baseUrl.auth}/organizations/${organization_uuid}`)
);

export const requestGetPipelines = (organization_uuid) => (
  ApiClient.get(`${baseUrl.app}/organizations/${organization_uuid}/pipelines`, appToken)
);

export const requestCreatePipeline = (organization_uuid, body) => (
  ApiClient.post(`/organizations/${organization_uuid}/pipelines`, body, 'app')
);

export const requestUpdatePipeline = (organization_uuid, pipeline_uuid, body) => (
  ApiClient.put(`/organizations/${organization_uuid}/pipelines/${pipeline_uuid}`, body, 'app')
);
