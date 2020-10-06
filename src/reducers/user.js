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
  CHANGE_ORGANIZATION,
} from 'actions';
import Auth from 'util/auth';

const DEFAULT_STATE = {
  profile: Auth.getUser(),
  currentOrg: null,
  createUserInProgress: false,
  createUserError: null,
  authInProgress: false,
  authError: null,
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case CREATE_USER:
      Auth.loginUser(action.payload);
      return {
        ...DEFAULT_STATE,
        profile: Auth.getUser(),
      };
    case CREATE_USER_IN_PROGRESS:
      return {
        ...DEFAULT_STATE,
        createUserInProgress: true,
      };
    case CREATE_USER_FAILED:
      return {
        ...DEFAULT_STATE,
        createUserError: action.payload,
      };
    case LOGIN_USER:
      Auth.loginUser(action.payload);
      return {
        ...DEFAULT_STATE,
        profile: Auth.getUser(),
      };
    case REFRESH_JWT: {
      const profile = {
        ...state.profile,
        token: action.payload.token,
      };

      Auth.loginUser(profile);
      return {
        ...DEFAULT_STATE,
        profile,
      };
    }
    case AUTH_IN_PROGRESS:
      Auth.logoutUser();
      return {
        ...DEFAULT_STATE,
        authInProgress: true,
      };
    case AUTH_FAILED:
      return {
        ...DEFAULT_STATE,
        authError: action.payload,
      };
    case LOGOUT_USER:
      Auth.logoutUser();
      return {
        ...DEFAULT_STATE,
      };
    case GET_USER_PROFILE: {
      const { organizations } = action.payload;
      return {
        ...state,
        profile: {
          ...state.profile,
          ...action.payload,
        },
        currentOrg: organizations && organizations.length ? organizations[0].uuid : state.currentOrg,
      };
    }
    case CHANGE_ORGANIZATION:
      return {
        ...state,
        currentOrg: action.payload,
      };
    default:
      return state;
  }
};
