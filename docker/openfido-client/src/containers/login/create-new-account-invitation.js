import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { Space } from 'antd';

import { createUser } from 'actions/user';
import { ROUTE_LOGIN } from 'config/routes';
import {
  Root,
  StyledH1,
  StyledH2,
  FormWrapper,
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
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
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
  }, [createUserInProgress, createUserError, formSubmitted, history, invitation_token]);

  const onEmailChanged = (e) => {
    setEmail(e.target.value);
  };

  const onFirstNameChanged = (e) => {
    setFirstName(e.target.value);
  };

  const onLastNameChanged = (e) => {
    setLastName(e.target.value);
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
        dispatch(createUser(email, firstName, lastName, password, invitation_token));
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
        You&apos;ve been invited to join
        <br />
        OpenFIDO
      </StyledH1>
      <FormWrapper>
        <StyledForm onSubmit={onCreateAccountClicked}>
          <StyledH2>
            Welcome to OpenFIDO.
            <br />
            Please create an account
          </StyledH2>
          <Space direction="vertical" size={-4}>
            <div>
              <StyledInput size="small" type="email" name="email" id="email" placeholder="email" onChange={onEmailChanged} />
              <FormMessage>
                <div />
                <StyledText color="pink">
                  {createUserError && 'Invalid email'}
                </StyledText>
              </FormMessage>
              <StyledInput size="small" type="text" name="first_name" id="first_name" placeholder="first name" onChange={onFirstNameChanged} />
              <FormMessage>
                <div />
                <StyledText color={createUserError && !firstName.length ? 'pink' : 'gray80'}>
                  Required
                </StyledText>
              </FormMessage>
              <StyledInput size="small" type="text" name="last_name" id="last_name" placeholder="last name" onChange={onLastNameChanged} />
              <FormMessage>
                <div />
                <StyledText color={createUserError && !lastName.length ? 'pink' : 'gray80'}>
                  Required
                </StyledText>
              </FormMessage>
              <StyledInput size="small" type="password" name="password" id="newPassword" placeholder="password" onChange={onPasswordChanged} />
              <FormMessage>
                <StyledText size="small" color="pink">{passwordMismatch && 'Passwords do not match'}</StyledText>
                <StyledText color={createUserError && password.length < 10 ? 'pink' : 'gray80'} float="right">
                  Minimum 10 characters
                </StyledText>
              </FormMessage>
              <StyledInput size="small" type="password" name="confirmPassword" id="confirmPassword" placeholder="re-enter password" onChange={onConfirmPasswordChanged} />
            </div>
            <Space direction="vertical" size={12}>
              <StyledButton
                htmlType="submit"
                size="middle"
                color="blue"
                width={106}
                role="button"
                tabIndex={0}
                onClick={onCreateAccountClicked}
              >
                <div>
                  Create
                  <br />
                  Account
                </div>
              </StyledButton>
              <Space direction="vertical" size={4} align="center">
                <FormMessage>
                  <StyledText size="small" color="pink" align="left">
                    {createUserError && !passwordMismatch && 'Please be sure to use the email address invitation was sent to'}
                  </StyledText>
                </FormMessage>
                <Link to={{ pathname: ROUTE_LOGIN, state: { invitation_token } }}>
                  <StyledText color="blue" fontweight={500}>Already a member? Log in</StyledText>
                </Link>
              </Space>
            </Space>
          </Space>
        </StyledForm>
      </FormWrapper>
    </Root>
  );
};

export default CreateNewAccountInvitation;
