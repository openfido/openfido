import {
  LOGIN_USER,
  LOGOUT_USER,
  REFRESH_JWT,
  AUTH_FAILED,
  AUTH_IN_PROGRESS,
} from 'actions';
import {
  requestLoginUser, requestRefreshJWT, requestUpdatePassword,
} from 'services';

export const loginUser = (email, password) => async (dispatch) => {
  await dispatch({ type: AUTH_IN_PROGRESS });
  requestLoginUser(email, password)
    .then((response) => {
      dispatch({
        type: LOGIN_USER,
        payload: response.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: AUTH_FAILED,
        payload: err.message,
      });
    });
};

export const refreshUserToken = (token) => (dispatch) => {
  requestRefreshJWT(token)
    .then((response) => {
      dispatch({
        type: REFRESH_JWT,
        payload: response.data,
      });
    })
    .catch(() => {
      // Treat as though we logged out. Very likely the user has reached the max
      // refresh timeout, and so needs to login again.
      dispatch({ type: LOGOUT_USER });
    });
};

export const logoutUser = () => ({
  type: LOGOUT_USER,
});

export const updatePassword = (email, reset_token, password) => async (dispatch) => {
  await dispatch({ type: AUTH_IN_PROGRESS });
  requestUpdatePassword(email, reset_token, password)
    .then((response) => {
      dispatch({
        type: LOGIN_USER,
        payload: response.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: AUTH_FAILED,
        payload: err.message,
      });
    });
};
