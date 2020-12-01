import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

import { loginUser } from 'actions/user';
import { acceptOrganizationInvitation } from 'actions/organization';
import { ROUTE_PIPELINES, ROUTE_RESET_PASSWORD } from 'config/routes';

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

const Login = () => {
  const history = useHistory();

  let invitation_token = null;
  if (history.location.state && 'invitation_token' in history.location.state) {
    invitation_token = history.location.state.invitation_token;
  }

  const profile = useSelector((state) => state.user.profile);
  const authInProgress = useSelector((state) => state.user.messages.authInProgress);
  const authError = useSelector((state) => state.user.messages.authError);
  const dispatch = useDispatch();

  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [formSubmitted, setFormSubmitted] = useState(false);

  useEffect(() => {
    if (profile) {
      if (invitation_token) {
        dispatch(acceptOrganizationInvitation(profile.uuid, invitation_token));
      }

      history.push(ROUTE_PIPELINES);
    }
  });

  const onEmailChanged = (e) => {
    setEmail(e.target.value);
  };

  const onPasswordChanged = (e) => {
    setPassword(e.target.value);
  };

  const onLoginClicked = (e) => {
    e.preventDefault();

    if (!authInProgress) {
      dispatch(loginUser(email, password));
      setFormSubmitted(true);
    }
  };

  return (
    <Root>
      <StyledH1>
        Welcome to
        <br />
        OpenFIDO
      </StyledH1>
      <FormWrapper>
        <StyledForm onSubmit={onLoginClicked}>
          <StyledH2>SIGN IN</StyledH2>
          <StyledInput
            aria-label="Email sign in input"
            type="email"
            placeholder="email"
            onChange={onEmailChanged}
          />
          <StyledInput
            aria-label="Password sign in input"
            type="password"
            placeholder="password"
            onChange={onPasswordChanged}
          />
          <FormMessage size="large">
            <StyledText
              size="middle"
              color="pink"
              float="left"
            >
              {authError && formSubmitted && 'Invalid credentials entered'}
            </StyledText>
            <StyledText
              size="middle"
              float="right"
            >
              <Link to={ROUTE_RESET_PASSWORD}>Forgot Password</Link>
            </StyledText>
          </FormMessage>
          <StyledButton
            htmlType="submit"
            size="middle"
            color="blue"
            width={108}
            role="button"
            tabIndex={0}
            onClick={onLoginClicked}
            onKeyPress={onLoginClicked}
          >
            Sign In
          </StyledButton>
        </StyledForm>
      </FormWrapper>
    </Root>
  );
};

export default Login;
