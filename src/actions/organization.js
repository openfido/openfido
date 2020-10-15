import {
  GET_ORGANIZATION_MEMBERS,
  REMOVE_ORGANIZATION_MEMBER,
  REMOVE_ORGANIZATION_MEMBER_FAILED,
  CHANGE_ORGANIZATION_MEMBER_ROLE,
  CHANGE_ORGANIZATION_MEMBER_ROLE_FAILED,
} from 'actions';
import {
  requestOrganizationMembers,
  requestRemoveOrganizationMember,
  requestChangeOrganizationMemberRole,
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
