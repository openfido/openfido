import {
  LOGIN_USER,
  LOGOUT_USER,
  REFRESH_JWT,
  AUTH_FAILED,
  AUTH_IN_PROGRESS,
  GET_USER_PROFILE,
  GET_USER_ORGANIZATIONS,
  CHANGE_ORGANIZATION,
} from 'actions';
import {
  requestLoginUser,
  requestRefreshJWT,
  requestUpdatePassword,
  requestUserProfile,
  requestUserOrganizations,
} from 'services';

export const loginUser = (email, password) => async (dispatch) => {
  await dispatch({ type: AUTH_IN_PROGRESS });
  requestLoginUser(email, password)
    .then((response) => {
      dispatch({
        type: LOGIN_USER,
        payload: response.data,
      });

      const { uuid } = response.data;
      return Promise.all([
        requestUserProfile(uuid),
        requestUserOrganizations(uuid),
      ]);
    })
    .then(([profileResponse, organizationsResponse]) => {
      dispatch({
        type: GET_USER_PROFILE,
        payload: profileResponse.data,
      });

      dispatch({
        type: GET_USER_ORGANIZATIONS,
        payload: organizationsResponse.data,
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

      return Promise.all([
        requestUserProfile(user_uuid),
        requestUserOrganizations(user_uuid),
      ]);
    })
    .then(([profileResponse, organizationsResponse]) => {
      dispatch({
        type: GET_USER_PROFILE,
        payload: profileResponse.data,
      });

      dispatch({
        type: GET_USER_ORGANIZATIONS,
        payload: organizationsResponse.data,
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

export const getUserOrganizations = (user_uuid) => (dispatch) => {
  requestUserOrganizations(user_uuid)
    .then((response) => {
      dispatch({
        type: GET_USER_ORGANIZATIONS,
        payload: response.data,
      });
    });
};
