import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';

import { loginUser } from 'actions/user';
import { ROUTE_PIPELINES, ROUTE_RESET_PASSWORD } from 'config/routes';

import { StyledButton, StyledText } from 'styles/app';
import colors from 'styles/colors';

const Root = styled.div`
  width: 100%;
  height: 100vh;
  text-align: center;
`;

const StyledH1 = styled.h1`
  font-size: 30px;
  font-size: 1.875rem;
  line-height: 36px;
  line-height: 2.25rem;
  font-weight: 400;
  padding-top: 100px;
  padding-top: 6.25rem;
  color: ${colors.white};
`;

const StyledH2 = styled.h2`
  font-size: 20px;
  font-size: 1.25rem;
  line-height: 24px;
  line-height: 1.5rem;
  color: ${colors.blue};
  text-transform: uppercase;
  margin-bottom: 40px;
  margin-bottom: 2.5rem;
`;

const StyledForm = styled.form`
  width: 390px;
  height: 522px;
  padding: 30px;
  margin: 42px auto 0 auto;
  margin: 2.625rem auto 0 auto;
  background-color: ${colors.white};
  text-align: left;
  border-radius: 3px;
`;

const StyledInput = styled.input`
  width: 330px;
  font-size: 18px;
  font-size: 1.125rem;
  color: ${colors.gray};
  padding-bottom: 0.625rem;
  padding-left: 0.25rem;
  padding-right: 0.25rem;
  border: none;
  border-bottom: 1px solid ${colors.lightGray};
  &::placeholder {
    color: ${colors.lightGray};
  }
  &:first-of-type {
    margin-bottom: 20px;
    margin-bottom: 1.25rem;
  }
`;

const LoginMessage = styled.div`
  padding: 0.75rem 0;
  height: 2.5rem;
  margin-bottom: 20px;
  margin-bottom: 1.25rem;
`;

const Login = () => {
  const history = useHistory();
  const profile = useSelector((state) => state.user.profile);
  const authInProgress = useSelector((state) => state.user.authInProgress);
  const authError = useSelector((state) => state.user.authError);
  const dispatch = useDispatch();

  const [email, setEmail] = useState();
  const [password, setPassword] = useState();

  useEffect(() => {
    if (profile) {
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
    }
  };

  return (
    <Root>
      <StyledH1>
        Welcome to
        <br />
        OpenFIDO
      </StyledH1>
      <StyledForm onSubmit={onLoginClicked}>
        <StyledH2>Sign In</StyledH2>
        <StyledInput type="email" placeholder="EMAIL" onChange={onEmailChanged} />
        <StyledInput type="password" placeholder="PASSWORD" onChange={onPasswordChanged} />
        <LoginMessage>
          <StyledText
            size="middle"
            color="pink"
            float="left"
          >
            {authError && 'Invalid credentials entered'}
          </StyledText>
          <StyledText
            size="middle"
            float="right"
          >
            <Link to={ROUTE_RESET_PASSWORD}>Forgot Password</Link>
          </StyledText>
        </LoginMessage>
        <StyledButton
          htmlType="submit"
          color="blue"
          width="108"
          role="button"
          tabIndex={0}
          onClick={onLoginClicked}
          onKeyPress={onLoginClicked}
        >
          Sign In
        </StyledButton>
      </StyledForm>
    </Root>
  );
};

export default Login;
