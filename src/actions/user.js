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
import {
  requestCreateUser,
  requestLoginUser,
  requestRefreshJWT,
  requestUpdatePassword,
  requestUserProfile,
} from 'services';

export const createUser = (organization_uuid, email, password, first_name, last_name) => async (dispatch) => {
  dispatch({ type: CREATE_USER_IN_PROGRESS });
  requestCreateUser(organization_uuid, email, password, first_name, last_name)
    .then((response) => {
      dispatch({
        type: CREATE_USER,
        payload: response.data,
      });

      return requestLoginUser(email, password);
    })
    .then((response) => {
      dispatch({
        type: LOGIN_USER,
        payload: response.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: CREATE_USER_FAILED,
        payload: err.message,
      });
    });
};

export const loginUser = (email, password) => async (dispatch) => {
  await dispatch({ type: AUTH_IN_PROGRESS });
  requestLoginUser(email, password)
    .then((response) => {
      dispatch({
        type: LOGIN_USER,
        payload: response.data,
      });

      const { uuid } = response.data;
      return requestUserProfile(uuid);
    })
    .then((response) => {
      dispatch({
        type: GET_USER_PROFILE,
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

export const refreshUserToken = (user_uuid) => (dispatch) => {
  requestRefreshJWT()
    .then((response) => {
      dispatch({
        type: REFRESH_JWT,
        payload: response.data,
      });

      return requestUserProfile(user_uuid);
    })
    .then((response) => {
      dispatch({
        type: GET_USER_PROFILE,
        payload: response.data,
      });
    })
    .catch(() => {
      // Treat as though we logged out. Very likely the user has reached the max
      // refresh timeout, and so needs to login again.
      dispatch({ type: LOGOUT_USER });
    });
};

export const getUserProfile = (user_uuid) => (dispatch) => {
  requestUserProfile(user_uuid)
    .then((response) => {
      dispatch({
        type: GET_USER_PROFILE,
        payload: response.data,
      });
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

export const changeOrganization = (organization_uuid) => ({
  type: CHANGE_ORGANIZATION,
  payload: organization_uuid,
});
