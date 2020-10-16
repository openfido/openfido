import {
  CREATE_USER,
  CREATE_USER_IN_PROGRESS,
  CREATE_USER_FAILED,
  LOGIN_USER,
  LOGOUT_USER,
  REFRESH_JWT,
  AUTH_FAILED,
  AUTH_IN_PROGRESS,
  CHANGE_ORGANIZATION,
  GET_USER_PROFILE,
  GET_USER_PROFILE_FAILED,
  GET_USER_ORGANIZATIONS,
  GET_USER_ORGANIZATIONS_FAILED,
  UPDATE_USER_PROFILE,
  UPDATE_USER_PROFILE_IN_PROGRESS,
  UPDATE_USER_PROFILE_FAILED,
  GET_USER_AVATAR,
  GET_USER_AVATAR_FAILED,
  UPDATE_USER_AVATAR,
  UPDATE_USER_AVATAR_FAILED,
  CHANGE_PASSWORD_IN_PROGRESS,
  CHANGE_PASSWORD,
  CHANGE_PASSWORD_FAILED,
  RETURN_TO_SETTINGS_CONFIRMED,
} from 'actions';
import {
  requestCreateUser,
  requestLoginUser,
  requestRefreshJWT,
  requestChangePassword,
  requestUserProfile,
  requestUserOrganizations,
  requestUpdateUserProfile,
  requestUserAvatar,
  requestUpdateUserAvatar,
} from 'services';

export const createUser = (email, firstName, lastName, password, invitation_token) => async (dispatch) => {
  await dispatch({ type: CREATE_USER_IN_PROGRESS });
  requestCreateUser(email, firstName, lastName, password, invitation_token)
    .then((response) => {
      dispatch({
        type: CREATE_USER,
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

      const { uuid: user_uuid } = response.data;

      requestUserProfile(user_uuid)
        .then((profileResponse) => {
          dispatch({
            type: GET_USER_PROFILE,
            payload: profileResponse.data,
          });
        })
        .catch(() => {
          dispatch({
            type: GET_USER_PROFILE_FAILED,
          });
        });

      requestUserOrganizations(user_uuid)
        .then((organizationsResponse) => {
          dispatch({
            type: GET_USER_ORGANIZATIONS,
            payload: organizationsResponse.data,
          });
        })
        .catch(() => {
          dispatch({
            type: GET_USER_ORGANIZATIONS_FAILED,
          });
        });

      requestUserAvatar(user_uuid)
        .then((avatarResponse) => {
          dispatch({
            type: GET_USER_AVATAR,
            payload: avatarResponse.data,
          });
        })
        .catch(() => {
          dispatch({
            type: GET_USER_AVATAR_FAILED,
          });
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

      requestUserProfile(user_uuid)
        .then((profileResponse) => {
          dispatch({
            type: GET_USER_PROFILE,
            payload: profileResponse.data,
          });
        })
        .catch(() => {
          dispatch({
            type: GET_USER_PROFILE_FAILED,
          });
        });

      requestUserOrganizations(user_uuid)
        .then((organizationsResponse) => {
          dispatch({
            type: GET_USER_ORGANIZATIONS,
            payload: organizationsResponse.data,
          });
        })
        .catch(() => {
          dispatch({
            type: GET_USER_ORGANIZATIONS_FAILED,
          });
        });

      requestUserAvatar(user_uuid)
        .then((avatarResponse) => {
          dispatch({
            type: GET_USER_AVATAR,
            payload: avatarResponse.data,
          });
        })
        .catch(() => {
          dispatch({
            type: GET_USER_AVATAR_FAILED,
          });
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

export const changeOrganization = (organization_uuid) => ({
  type: CHANGE_ORGANIZATION,
  payload: organization_uuid,
});

export const getUserProfile = (user_uuid) => (dispatch) => {
  requestUserProfile(user_uuid)
    .then((response) => {
      dispatch({
        type: GET_USER_PROFILE,
        payload: response.data,
      });
    });
};

export const updateUserAvatar = (user_uuid, image_content) => (dispatch) => {
  requestUpdateUserAvatar(user_uuid, image_content)
    .then(() => {
      dispatch({
        type: UPDATE_USER_AVATAR,
        payload: image_content,
      });

      return requestUserAvatar(user_uuid);
    })
    .then((response) => {
      dispatch({
        type: GET_USER_AVATAR,
        payload: response.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: UPDATE_USER_AVATAR_FAILED,
        payload: err.message,
      });
    });
};

export const updateUserProfile = (user_uuid, email, first_name, last_name) => async (dispatch) => {
  await dispatch({ type: UPDATE_USER_PROFILE_IN_PROGRESS });
  requestUpdateUserProfile(user_uuid, email, first_name, last_name)
    .then((response) => {
      dispatch({
        type: UPDATE_USER_PROFILE,
        payload: response.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: UPDATE_USER_PROFILE_FAILED,
        payload: err.message,
      });
    });
};

export const changePassword = (old_password, new_password) => async (dispatch) => {
  await dispatch({ type: CHANGE_PASSWORD_IN_PROGRESS });
  requestChangePassword(old_password, new_password)
    .then((response) => {
      dispatch({
        type: CHANGE_PASSWORD,
        payload: response.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: CHANGE_PASSWORD_FAILED,
        payload: err.message,
      });
    });
};

export const getUserOrganizations = (user_uuid) => (dispatch) => {
  requestUserOrganizations(user_uuid)
    .then((response) => {
      dispatch({
        type: GET_USER_ORGANIZATIONS,
        payload: response.data,
      });
    })
    .catch(() => {
      dispatch({
        type: GET_USER_ORGANIZATIONS_FAILED,
      });
    });
};

export const returnToSettingsConfirmed = () => ({
  type: RETURN_TO_SETTINGS_CONFIRMED,
});
