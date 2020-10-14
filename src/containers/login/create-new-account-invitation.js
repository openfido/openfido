import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';

import { createUser } from 'actions/user';
import { ROUTE_LOGIN } from 'config/routes';
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
  const history = useHistory();

  let invitation_token = null;
  if (history.location.state && 'invitation_token' in history.location.state) {
    invitation_token = history.location.state.invitation_token;
  }

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordMismatch, setPasswordMismatch] = useState(false);
  const [formSubmitted, setFormSubmitted] = useState(false);

  const createUserInProgress = useSelector((state) => state.user.messages.createUserInProgress);
  const createUserError = useSelector((state) => state.user.messages.createUserError);
  const dispatch = useDispatch();

  useEffect(() => {
    if (!createUserInProgress && !createUserError && formSubmitted) {
      history.push(ROUTE_LOGIN, { invitation_token });
    }
  }, [createUserInProgress, createUserError, formSubmitted, history]);

  const onEmailChanged = (e) => {
    setEmail(e.target.value);
  };

  const onPasswordChanged = (e) => {
    setPassword(e.target.value);
  };

  const onConfirmPasswordChanged = (e) => {
    setConfirmPassword(e.target.value);
  };

  const onCreateAccountClicked = (e) => {
    e.preventDefault();

    if (!createUserInProgress) {
      if (password === confirmPassword) {
        dispatch(createUser(email, password, invitation_token));
        setFormSubmitted(true);
        setPasswordMismatch(false);
      } else {
        setPasswordMismatch(true);
      }
    }
  };

  return (
    <Root>
      <StyledH1>
        You've been invited to join
        <br />
        OpenFIDO
      </StyledH1>
      <StyledForm onSubmit={onCreateAccountClicked}>
        <StyledH2>
          Welcome to OpenFIDO.
          <br />
          Please create an account
        </StyledH2>
        <StyledInput type="email" name="email" id="email" placeholder="email" onChange={onEmailChanged} />
        <FormMessage>
          <div />
          <StyledText color="pink">
            {createUserError && password.length < 10 && 'Invalid email'}
          </StyledText>
        </FormMessage>
        <StyledInput type="password" name="password" id="newPassword" placeholder="password" onChange={onPasswordChanged} />
        <FormMessage>
          <StyledText size="small" color="pink">{passwordMismatch && 'Passwords do not match'}</StyledText>
          <StyledText color={createUserError && password.length < 10 ? 'pink' : 'gray80'} float="right">
            Minimum 10 characters
          </StyledText>
        </FormMessage>
        <StyledInput type="password" name="confirmPassword" id="confirmPassword" placeholder="re-enter password" onChange={onConfirmPasswordChanged} />
        <FormMessage size="large" />
        <StyledButton
          htmlType="submit"
          size="middle"
          color="blue"
          width={106}
          role="button"
          tabIndex={0}
          onClick={onCreateAccountClicked}
        >
          <label>
            Create
            <br />
            Account
          </label>
        </StyledButton>
        <FormMessage size="middle">
          <Link to={{ pathname: ROUTE_LOGIN, state: { invitation_token } }}>
            <StyledButton
              htmlType="button"
              size="small"
              type="text"
            >
              Already have an account?
            </StyledButton>
          </Link>
        </FormMessage>
        <br />
        <FormMessage size="small">
          {createUserError && !passwordMismatch && (
          <StyledText size="small" color="pink">
            Please be sure to use the email address invitation was sent to
          </StyledText>
          )}
        </FormMessage>
      </StyledForm>
    </Root>
  );
};

export default CreateNewAccountInvitation;
