import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { createUser } from 'actions/user';
import {
  Root,
  StyledH1,
  StyledH2,
  StyledForm,
  StyledInput,
  FormMessage,
} from 'styles/login';
import { StyledButton, StyledText } from 'styles/app';

const CreateNewAccountInvitation = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordMismatch, setPasswordMismatch] = useState(false);

  const invitationOrganization = useSelector((state) => state.organization.invitationOrganization);
  const createUserInProgress = useSelector((state) => state.user.messages.createUserInProgress);
  const createUserError = useSelector((state) => state.user.messages.createUserError);
  const dispatch = useDispatch();

  const onEmailChanged = (e) => {
    setEmail(e.target.value);
  };

  const onPasswordChanged = (e) => {
    setPassword(e.target.value);
  };

  const onConfirmPasswordChanged = (e) => {
    setConfirmPassword(e.target.value);
  };

  const onSignInClicked = (e) => {
    e.preventDefault();
    if (password === confirmPassword) {
      dispatch(createUser(invitationOrganization, email, password));
      setPasswordMismatch(false);
    } else {
      setPasswordMismatch(true);
    }
  };

  return (
    <Root>
      <StyledH1>
        You've been invited to join
        <br />
        OpenFIDO
      </StyledH1>
      <StyledForm onSubmit={onSignInClicked}>
        <StyledH2>
          Welcome to OpenFIDO.
          <br />
          Please create an account
        </StyledH2>
        <StyledInput type="email" name="email" id="email" placeholder="email" onChange={onEmailChanged} />
        <StyledInput type="password" name="password" id="newPassword" placeholder="password" onChange={onPasswordChanged} />
        <FormMessage>
          <StyledText size="small" color="pink">{passwordMismatch && 'Passwords do not match'}</StyledText>
          <StyledText color={createUserError && password.length < 10 ? 'pink' : 'gray80'} float="right">
            Minimum 10 characters
          </StyledText>
        </FormMessage>
        <StyledInput type="password" name="confirmPassword" id="confirmPassword" placeholder="re-enter password" onChange={onConfirmPasswordChanged} />
        <FormMessage size="large">
          {createUserError && !passwordMismatch && (
            <StyledText size="small" color="pink">Could not create account.</StyledText>
          )}
        </FormMessage>
        <StyledButton
          htmlType="submit"
          color="blue"
          width={106}
          role="button"
          tabIndex={0}
          onClick={onSignInClicked}
          loading={createUserInProgress}
        >
          Sign In
        </StyledButton>
      </StyledForm>
    </Root>
  );
};

export default CreateNewAccountInvitation;
