import {
  GET_ORGANIZATION_MEMBERS,
  REMOVE_ORGANIZATION_MEMBER,
  REMOVE_ORGANIZATION_MEMBER_FAILED,
  CHANGE_ORGANIZATION_MEMBER_ROLE,
  CHANGE_ORGANIZATION_MEMBER_ROLE_FAILED,
  INVITE_ORGANIZATION_MEMBER,
  INVITE_ORGANIZATION_MEMBER_FAILED,
  ACCEPT_ORGANIZATION_INVITATION,
  ACCEPT_ORGANIZATION_INVITATION_FAILED,
} from 'actions';
import {
  requestOrganizationMembers,
  requestRemoveOrganizationMember,
  requestChangeOrganizationMemberRole,
  requestInviteOrganizationMember,
  requestAcceptOrganizationInvitation,
} from 'services';

export const getOrganizationMembers = (organization_uuid) => async (dispatch) => {
  requestOrganizationMembers(organization_uuid)
    .then((response) => {
      dispatch({
        type: GET_ORGANIZATION_MEMBERS,
        payload: response.data,
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
          removeMemberError: err.message,
        },
      });
    });
};

export const changeOrganizationMemberRole = (organization_uuid, user_uuid, role) => async (dispatch) => {
  requestChangeOrganizationMemberRole(organization_uuid, user_uuid, role)
    .then(() => {
      dispatch({
        type: CHANGE_ORGANIZATION_MEMBER_ROLE,
        payload: user_uuid,
      });
    })
    .catch((err) => {
      dispatch({
        type: CHANGE_ORGANIZATION_MEMBER_ROLE_FAILED,
        payload: {
          userRoleChanged: user_uuid,
          changeRoleError: err.message,
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
          inviteOrganizationMemberError: err.message,
        },
      });
    });
};

export const acceptOrganizationInvitation = (organization_uuid, invitation_token) => async (dispatch) => {
  requestAcceptOrganizationInvitation(organization_uuid, invitation_token)
    .then(() => {
      dispatch({
        type: ACCEPT_ORGANIZATION_INVITATION,
        payload: invitation_token,
      });
    })
    .catch((err) => {
      dispatch({
        type: ACCEPT_ORGANIZATION_INVITATION_FAILED,
        payload: {
          acceptInvitationError: err.message,
        },
      });
    });
};
