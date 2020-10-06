import {
  GET_ORGANIZATION_MEMBERS,
  REMOVE_ORGANIZATION_MEMBER,
  REMOVE_ORGANIZATION_MEMBER_FAILED,
} from 'actions';

const DEFAULT_STATE = {
  members: null,
  userRemoved: null,
  removeMemberError: null,
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case GET_ORGANIZATION_MEMBERS:
      return {
        ...DEFAULT_STATE,
        members: action.payload,
      };
    case REMOVE_ORGANIZATION_MEMBER:
      return {
        ...DEFAULT_STATE,
        members: state.members.filter((item) => action.payload !== item.uuid),
        ...action.payload,
      };
    case REMOVE_ORGANIZATION_MEMBER_FAILED:
      return {
        ...state,
        ...action.payload,
      };
    default:
      return state;
  }
};
