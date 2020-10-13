import React, { useState, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Space } from 'antd';
import styled from 'styled-components';

import { changePassword, changePasswordConfirmed } from 'actions/user';
import { StyledText, StyledInput, StyledButton } from 'styles/app';
import ChangePasswordSuccessPopup from './change-password-success-popup';

const StyledForm = styled.form`
  display: grid;
  grid-gap: 16px;
  grid-gap: 1rem;
  max-width: 432px;
  button[type="submit"], button[type="reset"] {
    margin-top: 32px;
    margin-top: 2rem;
  }
  label {
    position: relative;
  }
`;

const FormMessage = styled.div`
  ${({ size, align }) => (`
  ${size === 'small' ? (`
  width: 100%;
  position: absolute;
  text-align: right;
  `) : (`
  margin-top: 32px;
  margin-top: 2rem;
  `)}
  ${align ? (`
  text-align: ${align};
  `) : ''}
  `)}
`;

const EditProfile = () => {
  const oldPasswordInput = useRef();

  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordMismatch, setPasswordMismatch] = useState(false);

  const profile = useSelector((state) => state.user.profile);
  const changePasswordSuccess = useSelector((state) => state.user.messages.changePasswordSuccess);
  const changePasswordInProgress = useSelector((state) => state.user.messages.changePasswordInProgress);
  const changePasswordError = useSelector((state) => state.user.messages.changePasswordError);
  const dispatch = useDispatch();

  if (!profile) return null;

  const onChangePasswordClicked = (e) => {
    e.preventDefault();

    if (newPassword === confirmPassword) {
      if (!changePasswordInProgress) {
        dispatch(changePassword(oldPassword, newPassword));
        setPasswordMismatch(false);
        setOldPassword('');
        setNewPassword('');
        setConfirmPassword('');
        if (oldPasswordInput.current) oldPasswordInput.current.focus();
      }
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

  const onReturnToSettingsClicked = () => {
    dispatch(changePasswordConfirmed());
  };

  return (
    <>
      <StyledForm>
        <label htmlFor="old_password">
          <StyledText display="block" color="darkText">Old Password</StyledText>
          <StyledInput
            ref={oldPasswordInput}
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
          <FormMessage size="small">
            <StyledText size="small" color={changePasswordError && newPassword.length < 10 ? 'pink' : 'gray80'}>
              minimum 10 characters
            </StyledText>
          </FormMessage>
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
          <FormMessage size="small" align="left">
            <StyledText size="small" color="pink">
              {passwordMismatch && 'Passwords do not match'}
            </StyledText>
          </FormMessage>
        </label>
        <Space direction="horizontal" size={24}>
          <StyledButton
            htmlType="submit"
            size="middle"
            color="blue"
            width={152}
            role="button"
            tabIndex={0}
            onClick={onChangePasswordClicked}
          >
            Change Password
          </StyledButton>
          <StyledButton
            htmlType="reset"
            type="text"
            height={50}
            onClick={onCancelClicked}
          >
            Cancel
          </StyledButton>
          <FormMessage size="large">
            {changePasswordError && (
              <StyledText size="small" color="pink">Password could not be changed.</StyledText>
            )}
          </FormMessage>
        </Space>
      </StyledForm>
      {changePasswordSuccess && !changePasswordError && !passwordMismatch && (
        <ChangePasswordSuccessPopup
          handleOk={onReturnToSettingsClicked}
          handleCancel={onReturnToSettingsClicked}
        />
      )}
    </>
  );
};

export default EditProfile;
