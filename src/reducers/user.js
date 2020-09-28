import {
  LOGIN_USER_STARTED,
  LOGIN_USER_COMPLETED,
  LOGIN_USER_FAILED,
  LOGOUT_USER,
} from 'actions';
import Auth from 'util/auth';

const DEFAULT_STATE = {
  profile: null,
  isLoggingIn: false,
  loginError: null,
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case LOGIN_USER_STARTED:
      Auth.logoutUser();
      return {
        ...DEFAULT_STATE,
        isLoggingIn: true,
      };
    case LOGIN_USER_COMPLETED:
      Auth.loginUser(action.payload);
      return {
        ...DEFAULT_STATE,
        profile: Auth.getUser(),
      };
    case LOGIN_USER_FAILED:
      return {
        ...DEFAULT_STATE,
        loginError: action.payload,
      };
    case LOGOUT_USER:
      Auth.logoutUser();
      return DEFAULT_STATE;
    default:
      return state;
  }
};
