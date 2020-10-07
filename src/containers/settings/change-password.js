import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Space } from 'antd';
import styled from 'styled-components';

import { changePassword } from 'actions/user';
import { StyledText, StyledInput, StyledButton } from 'styles/app';

const StyledForm = styled.form`
  display: grid;
  grid-gap: 16px;
  grid-gap: 1rem;
  button[type="submit"], button[type="reset"] {
    margin-top: 32px;
    margin-top: 2rem;
  }
  input {
    width: 432px;
  }
`;

const FormMessage = styled.div`
  width: 432px;
  margin-top: 32px;
  margin-top: 2rem;
`;


const EditProfile = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const profile = useSelector((state) => state.user.profile);
  const changePasswordSuccess = useSelector((state) => state.user.messages.changePasswordSuccess);
  const changePasswordInProgress = useSelector((state) => state.user.messages.changePasswordInProgress);
  const changePasswordError = useSelector((state) => state.user.messages.changePasswordError);
  const [passwordMismatch, setPasswordMismatch] = useState(false);
  const dispatch = useDispatch();

  if (!profile) return null;

  const onChangePasswordClicked = (e) => {
    e.preventDefault();
    if (newPassword === confirmPassword) {
      dispatch(changePassword(profile.uuid, oldPassword, newPassword));
      setPasswordMismatch(false);
    } else {
      setPasswordMismatch(true);
    }
  };

  const onCancelClicked = (e) => {
    e.preventDefault();
    setOldPassword('');
    setNewPassword('');
    setConfirmPassword('');
  };

  const onOldPasswordChanged = (e) => {
    setOldPassword(e.target.value);
  };

  const onNewPasswordChanged = (e) => {
    setNewPassword(e.target.value);
  };

  const onConfirmPasswordChanged = (e) => {
    setConfirmPassword(e.target.value);
  };

  return (
    <StyledForm>
      <label htmlFor="old_password">
        <StyledText display="block" color="darkText">Old Password</StyledText>
        <StyledInput
          type="password"
          bgcolor="white"
          size="large"
          name="old_password"
          id="old_password"
          value={oldPassword}
          onChange={onOldPasswordChanged}
        />
      </label>
      <label htmlFor="new_password">
        <StyledText display="block" color="darkText">New Password</StyledText>
        <StyledInput
          type="password"
          bgcolor="white"
          size="large"
          name="new_password"
          id="new_password"
          value={newPassword}
          onChange={onNewPasswordChanged}
        />
      </label>
      <label htmlFor="email">
        <StyledText display="block" color="darkText">Confirm Password</StyledText>
        <StyledInput
          type="password"
          bgcolor="white"
          size="large"
          name="confirm_password"
          id="confirm_password"
          value={confirmPassword}
          onChange={onConfirmPasswordChanged}
        />
      </label>
      <Space direction="horizontal" size={24}>
        <StyledButton
          htmlType="submit"
          size="middle"
          color="blue"
          width={128}
          role="button"
          tabIndex={0}
          loading={changePasswordInProgress}
          onClick={onChangePasswordClicked}
        >
          Update Profile
        </StyledButton>
        <StyledButton
          htmlType="reset"
          type="text"
          height={50}
          onClick={onCancelClicked}
        >
          Cancel
        </StyledButton>
        <FormMessage>
          {changePasswordSuccess && !changePasswordError && !passwordMismatch && (
            <StyledText size="middle" color="green">Password changed.</StyledText>
          )}
          {changePasswordError && (
            <StyledText size="middle" color="pink">Password could not be changed.</StyledText>
          )}
          {!changePasswordError && passwordMismatch && (
            <StyledText size="middle" color="pink">Passwords do not match</StyledText>
          )}
        </FormMessage>
      </Space>
    </StyledForm>
  );
};

export default EditProfile;
