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
  GET_ORGANIZATION_INVITATIONS,
  GET_ORGANIZATION_MEMBERS_INVITATIONS_FAILED,
} from 'actions';

const DEFAULT_STATE = {
  members: null,
  invitations: [],
  messages: {
    userRemoved: null,
    removeMemberError: null,
    userRoleChanged: null,
    changeRoleError: null,
    userInvited: null,
    inviteOrganizationMemberError: null,
    invitationOrganization: null,
    invitationToken: null,
    acceptInvitationError: null,
  },
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case GET_ORGANIZATION_MEMBERS:
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        members: action.payload,
      };
    case REMOVE_ORGANIZATION_MEMBER:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          userRemoved: action.payload,
        },
        members: state.members.filter((item) => action.payload !== item.uuid),
      };
    case REMOVE_ORGANIZATION_MEMBER_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          ...action.payload,
        },
        members: state.members,
      };
    case CHANGE_ORGANIZATION_MEMBER_ROLE: {
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
      };
    }
    case CHANGE_ORGANIZATION_MEMBER_ROLE_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          ...action.payload,
        },
        members: state.members,
      };
    case INVITE_ORGANIZATION_MEMBER:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          userInvited: action.payload,
        },
        members: state.members,
      };
    case INVITE_ORGANIZATION_MEMBER_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          ...action.payload,
        },
        members: state.members,
      };
    case ACCEPT_ORGANIZATION_INVITATION:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          ...action.payload,
        },
        members: state.members,
      };
    case ACCEPT_ORGANIZATION_INVITATION_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          ...action.payload,
        },
        members: state.members,
      };
    case GET_ORGANIZATION_INVITATIONS:
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        members: state.members,
        invitations: action.payload,
      };
    case GET_ORGANIZATION_MEMBERS_INVITATIONS_FAILED:
      return {
        ...DEFAULT_STATE,
      };
    default:
      return state;
  }
};
