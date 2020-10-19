import {
  GET_ORGANIZATION_MEMBERS,
  GET_ORGANIZATION_MEMBERS_FAILED,
  REMOVE_ORGANIZATION_MEMBER,
  REMOVE_ORGANIZATION_MEMBER_FAILED,
  CHANGE_ORGANIZATION_MEMBER_ROLE,
  CHANGE_ORGANIZATION_MEMBER_ROLE_FAILED,
  INVITE_ORGANIZATION_MEMBER,
  INVITE_ORGANIZATION_MEMBER_FAILED,
  ACCEPT_ORGANIZATION_INVITATION,
  ACCEPT_ORGANIZATION_INVITATION_FAILED,
  GET_ORGANIZATION_INVITATIONS,
  GET_ORGANIZATION_MEMBERS_INVITATIONS_FAILED,
  GET_USER_ORGANIZATIONS,
  GET_USER_ORGANIZATIONS_FAILED,
  CHANGE_ORGANIZATION,
} from 'actions';
import {
  requestOrganizationMembers,
  requestOrganizationInvitations,
  requestRemoveOrganizationMember,
  requestChangeOrganizationMemberRole,
  requestInviteOrganizationMember,
  requestAcceptOrganizationInvitation,
  requestUserOrganizations,
} from 'services';

export const getOrganizationMembers = (organization_uuid) => async (dispatch) => {
  requestOrganizationMembers(organization_uuid)
    .then((membersResponse) => {
      dispatch({
        type: GET_ORGANIZATION_MEMBERS,
        payload: membersResponse.data,
      });

      requestOrganizationInvitations(organization_uuid)
        .then((invitationsResponse) => {
          dispatch({
            type: GET_ORGANIZATION_INVITATIONS,
            payload: invitationsResponse.data,
          });
        })
        .catch((err) => {
          dispatch({
            type: GET_ORGANIZATION_MEMBERS_INVITATIONS_FAILED,
            payload: err.response.data,
          });
        });
    })
    .catch((err) => {
      dispatch({
        type: GET_ORGANIZATION_MEMBERS_FAILED,
        payload: err.response.data,
      });
    });
};

export const removeOrganizationMember = (organization_uuid, user_uuid) => async (dispatch) => {
  // organization_uuid === currentOrg
  requestRemoveOrganizationMember(organization_uuid, user_uuid)
    .then(() => {
      dispatch({
        type: REMOVE_ORGANIZATION_MEMBER,
        payload: user_uuid,
      });
    })
    .catch((err) => {
      dispatch({
        type: REMOVE_ORGANIZATION_MEMBER_FAILED,
        payload: {
          userRemoved: user_uuid,
          removeMemberError: err.response.data,
        },
      });
    });
};

export const changeOrganizationMemberRole = (organization_uuid, user_uuid, role) => async (dispatch) => {
  requestChangeOrganizationMemberRole(organization_uuid, user_uuid, role)
    .then(() => {
      dispatch({
        type: CHANGE_ORGANIZATION_MEMBER_ROLE,
        payload: {
          user_uuid,
          role,
        },
      });

      requestOrganizationMembers(organization_uuid)
        .then((membersResponse) => {
          dispatch({
            type: GET_ORGANIZATION_MEMBERS,
            payload: membersResponse.data,
          });
        })
        .catch(() => {
          dispatch({
            type: GET_ORGANIZATION_MEMBERS_FAILED,
          });
        });
    })
    .catch((err) => {
      dispatch({
        type: CHANGE_ORGANIZATION_MEMBER_ROLE_FAILED,
        payload: {
          userRoleChanged: user_uuid,
          changeRoleError: err.response.data,
        },
      });
    });
};

export const inviteOrganizationMember = (organization_uuid, email) => async (dispatch) => {
  requestInviteOrganizationMember(organization_uuid, email)
    .then(() => {
      dispatch({
        type: INVITE_ORGANIZATION_MEMBER,
        payload: email,
      });
    })
    .catch((err) => {
      dispatch({
        type: INVITE_ORGANIZATION_MEMBER_FAILED,
        payload: {
          userInvited: email,
          inviteOrganizationMemberError: err.response.data,
        },
      });
    });
};

export const acceptOrganizationInvitation = (user_uuid, invitation_token) => async (dispatch) => {
  requestAcceptOrganizationInvitation(invitation_token)
    .then((invitationsResponse) => {
      const { organization_uuid } = invitationsResponse.data;

      dispatch({
        type: ACCEPT_ORGANIZATION_INVITATION,
        payload: {
          invitationOrganization: organization_uuid,
          invitationToken: invitation_token,
        },
      });

      dispatch({
        type: CHANGE_ORGANIZATION,
        payload: organization_uuid,
      });

      requestUserOrganizations(user_uuid)
        .then((organizationsResponse) => {
          dispatch({
            type: GET_USER_ORGANIZATIONS,
            payload: organizationsResponse.data,
          });
        })
        .catch(() => {
          dispatch({
            type: GET_USER_ORGANIZATIONS_FAILED,
          });
        });
    })
    .catch((err) => {
      dispatch({
        type: ACCEPT_ORGANIZATION_INVITATION_FAILED,
        payload: {
          invitationToken: invitation_token,
          acceptInvitationError: err.response.data,
        },
      });
    });
};
