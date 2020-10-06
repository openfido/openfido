import {
  CREATE_USER,
  CREATE_USER_IN_PROGRESS,
  CREATE_USER_FAILED,
  LOGIN_USER,
  LOGOUT_USER,
  REFRESH_JWT,
  AUTH_FAILED,
  AUTH_IN_PROGRESS,
  GET_USER_PROFILE,
  UPDATE_USER_PROFILE,
  UPDATE_USER_PROFILE_FAILED,
  GET_USER_AVATAR,
  UPDATE_USER_AVATAR,
  UPDATE_USER_AVATAR_FAILED,
  CHANGE_ORGANIZATION,
} from 'actions';
import Auth from 'util/auth';

const DEFAULT_STATE = {
  profile: Auth.getUser(),
  avatar: 'data:image/jpg;base64,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',
  currentOrg: null,
  messages: {
    createUserInProgress: false,
    createUserError: null,
    authInProgress: false,
    authError: null,
    updateUserProfileError: null,
    updateUserAvatarError: null,
  },
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case CREATE_USER:
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
      };
    case CREATE_USER_IN_PROGRESS:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          createUserInProgress: true,
        },
      };
    case CREATE_USER_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          createUserError: action.payload,
        },
      };
    case LOGIN_USER:
      Auth.loginUser(action.payload);
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        profile: Auth.getUser(),
      };
    case REFRESH_JWT: {
      const profile = {
        ...state.profile,
        token: action.payload.token,
      };

      Auth.loginUser(profile);
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        profile,
      };
    }
    case AUTH_IN_PROGRESS:
      Auth.logoutUser();
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          authInProgress: true,
        },
        profile: null,
      };
    case AUTH_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          authError: action.payload,
        },
        profile: null,
      };
    case LOGOUT_USER:
      Auth.logoutUser();
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        profile: null,
      };
    case GET_USER_PROFILE: {
      const { organizations } = action.payload;
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        profile: {
          ...state.profile,
          ...action.payload,
        },
        currentOrg: organizations && organizations.length ? organizations[0].uuid : state.currentOrg,
      };
    }
    case UPDATE_USER_PROFILE: {
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        profile: action.payload,
      };
    }
    case UPDATE_USER_PROFILE_FAILED: {
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          updateUserProfileError: action.payload,
        }
      };
    }
    case GET_USER_AVATAR: {
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        avatar: action.payload,
      };
    }
    case UPDATE_USER_AVATAR: {
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        avatar: action.payload,
      };
    }
    case UPDATE_USER_AVATAR_FAILED: {
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          updateUserAvatarError: action.payload,
        },
      };
    }
    case CHANGE_ORGANIZATION:
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        currentOrg: action.payload,
      };
    default:
      return state;
  }
};
