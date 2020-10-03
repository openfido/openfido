import {
  GET_ORGANIZATION_MEMBERS,
  REMOVE_ORGANIZATION_MEMBER,
  REMOVE_ORGANIZATION_MEMBER_FAILED,
} from 'actions';
import {
  requestOrganizationMembers,
  requestRemoveOrganizationMember,
} from 'services';

export const getOrganizationMembers = (organization_uuid, token) => async (dispatch) => {
  requestOrganizationMembers(organization_uuid, token)
    .then((response) => {
      dispatch({
        type: GET_ORGANIZATION_MEMBERS,
        payload: response.data,
      });
    });
};

export const removeOrganizationMember = (organization_uuid, user_uuid, token) => async (dispatch) => {
  // organization_uuid === currentOrg
  requestRemoveOrganizationMember(organization_uuid, user_uuid, token)
    .then(() => {
      dispatch({
        type: REMOVE_ORGANIZATION_MEMBER,
        payload: user_uuid,
      });
    })
    .catch((err) => {
      dispatch({
        type: REMOVE_ORGANIZATION_MEMBER_FAILED,
        payload: err.message,
      });
    });
};
