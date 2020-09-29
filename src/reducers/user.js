import {
  LOGIN_USER,
  LOGOUT_USER,
  REFRESH_JWT,
  AUTH_FAILED,
  AUTH_IN_PROGRESS,
} from 'actions';

const DEFAULT_STATE = {
  profile: null,
  authInProgress: false,
  authError: null,
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case LOGIN_USER:
      return {
        ...DEFAULT_STATE,
        profile: action.payload,
      };
    case REFRESH_JWT:
      return {
        ...DEFAULT_STATE,
        profile: {
          ...state.profile,
          token: action.payload.token,
        },
      };
    case AUTH_IN_PROGRESS:
      return {
        ...DEFAULT_STATE,
        authInProgress: true,
        profile: null,
      };
    case AUTH_FAILED:
      return {
        ...DEFAULT_STATE,
        authError: action.payload,
        profile: null,
      };
    case LOGOUT_USER:
      return DEFAULT_STATE;
    default:
      return state;
  }
};
