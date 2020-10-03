import {
  GET_ORGANIZATION_MEMBERS,
  REMOVE_ORGANIZATION_MEMBER,
} from 'actions';
import {
  requestOrganizationMembers,
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

export const removeOrganizationMember = (organization_uuid, user_uuid) => async (dispatch) => {
};
