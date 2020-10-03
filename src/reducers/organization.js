import {
  GET_ORGANIZATION_MEMBERS,
  REMOVE_ORGANIZATION_MEMBER,
  REMOVE_ORGANIZATION_MEMBER_FAILED,
  CHANGE_ORGANIZATION_MEMBER_ROLE,
  CHANGE_ORGANIZATION_MEMBER_ROLE_FAILED,
} from 'actions';

const DEFAULT_STATE = {
  members: null,
  userRemoved: null,
  removeMemberError: null,
  changeRoleError: null,
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
        userRemoved: action.payload,
      };
    case REMOVE_ORGANIZATION_MEMBER_FAILED:
      return {
        ...state,
        ...action.payload,
      };
    case CHANGE_ORGANIZATION_MEMBER_ROLE: {
      const member = state.members.find((item) => action.payload === item.uuid);
      const { members } = state;

      if (member) {
        member.role.name = action.payload;
      }

      return {
        ...state,
        members,
      };
    }
    case CHANGE_ORGANIZATION_MEMBER_ROLE_FAILED:
      return {
        ...state,
        changeRoleError: true,
      };
    default:
      return state;
  }
};
