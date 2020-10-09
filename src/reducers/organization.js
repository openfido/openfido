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
} from 'actions';

const DEFAULT_STATE = {
  members: null,
  userRemoved: null,
  removeMemberError: null,
  userRoleChanged: null,
  changeRoleError: null,
  userInvited: null,
  inviteOrganizationMemberError: null,
  invitationOrganization: null,
  invitationToken: null,
  acceptInvitationError: null,
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
        ...DEFAULT_STATE,
        members: state.members,
        ...action.payload,
      };
    case CHANGE_ORGANIZATION_MEMBER_ROLE: {
      const member = state.members.find((item) => action.payload === item.uuid);
      const { members } = state;

      if (member && member.role) {
        member.role.name = action.payload;
      }

      return {
        ...DEFAULT_STATE,
        members,
        userRoleChanged: action.payload,
      };
    }
    case CHANGE_ORGANIZATION_MEMBER_ROLE_FAILED:
      return {
        ...DEFAULT_STATE,
        members: state.members,
        ...action.payload,
      };
    case INVITE_ORGANIZATION_MEMBER:
      return {
        ...DEFAULT_STATE,
        members: state.members,
        userInvited: action.payload,
      };
    case INVITE_ORGANIZATION_MEMBER_FAILED:
      return {
        ...DEFAULT_STATE,
        members: state.members,
        ...action.payload,
      };
    case ACCEPT_ORGANIZATION_INVITATION:
      return {
        ...DEFAULT_STATE,
        members: state.members,
        ...action.payload,
      };
    case ACCEPT_ORGANIZATION_INVITATION_FAILED:
      return {
        ...DEFAULT_STATE,
        members: state.members,
        ...action.payload,
      };
    case GET_ORGANIZATION_INVITATIONS:
      return {
        ...DEFAULT_STATE,
        members: state.members,
        invitations: action.payload,
      };
    default:
      return state;
  }
};
