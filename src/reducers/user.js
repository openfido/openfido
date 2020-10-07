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
  avatar: null,
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
        profile: {
          ...state.profile,
          ...action.payload,
        },
      };
    }
    case UPDATE_USER_PROFILE_FAILED: {
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          updateUserProfileError: action.payload,
        },
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
