import {
  LOGIN_USER,
  LOGOUT_USER,
  REFRESH_JWT,
  AUTH_FAILED,
  AUTH_IN_PROGRESS,
} from 'actions';
import Auth from 'util/auth';

const DEFAULT_STATE = {
  profile: Auth.getUser(),
  authInProgress: false,
  authError: null,
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case LOGIN_USER:
      Auth.loginUser(action.payload);
      return {
        ...DEFAULT_STATE,
        profile: Auth.getUser(),
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
      Auth.logoutUser();
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
      Auth.logoutUser();
      return {
        ...DEFAULT_STATE,
        profile: null,
      };
    default:
      return state;
  }
};
