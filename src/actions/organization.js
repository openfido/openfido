import {
  GET_ORGANIZATION_MEMBERS,
  REMOVE_ORGANIZATION_MEMBER,
  REMOVE_ORGANIZATION_MEMBER_FAILED,
} from 'actions';
import {
  requestOrganizationMembers,
  requestRemoveOrganizationMember,
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
        payload: {
          userRemoved: user_uuid,
        },
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
