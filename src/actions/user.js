import {
  LOGIN_USER_STARTED,
  LOGIN_USER_COMPLETED,
  LOGIN_USER_FAILED,
  LOGOUT_USER,
} from 'actions';
import ApiClient from 'util/api-client';

export function loginUserStarted() {
  return {
    type: LOGIN_USER_STARTED,
  };
}

export function loginUserCompleted(payload) {
  return {
    type: LOGIN_USER_COMPLETED,
    payload,
  };
}

export function loginUserFailed(error) {
  return {
    type: LOGIN_USER_FAILED,
    payload: error,
  };
}

export function loginUser(email, password) {
  return (dispatch) => {
    dispatch(loginUserStarted());
    try {
      ApiClient.post('/users/auth', { email, password })
        .then((res) => {
          const user = res.data;
          if (email === user.email) {
            dispatch(loginUserCompleted(user));
          } else {
            throw Error('Incorrect email and password');
          }
        })
        .catch((err) => {
          dispatch(loginUserFailed(err));
        });
    } catch (err) {
      dispatch(loginUserFailed(err));
    }
  };
}

export function logoutUser() {
  return {
    type: LOGOUT_USER,
  };
}
