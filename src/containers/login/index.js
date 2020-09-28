import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import styled from 'styled-components';

import { loginUser as loginUserAction } from 'actions/user';
import { ROUTE_PIPELINES, ROUTE_FORGOT_PASSWORD } from 'config/routes';

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

const Login = ({
  loginUser, isLoggingIn, loginError, userProfile
}) => {
  const history = useHistory();

  const [email, setEmail] = useState();
  const [password, setPassword] = useState();

  useEffect(() => {
    if (userProfile) {
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

    if (!isLoggingIn) {
      loginUser(email, password);
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
        <StyledInput placeholder="EMAIL" onChange={onEmailChanged} />
        <StyledInput type="password" placeholder="PASSWORD" onChange={onPasswordChanged} />
        <LoginMessage>
          <StyledText
            size="middle"
            color="pink"
            float="left"
          >
            {loginError && 'Invalid credentials entered'}
          </StyledText>
          <StyledText
            size="middle"
            float="right"
          >
            <Link to={ROUTE_FORGOT_PASSWORD}>Forgot Password</Link>
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

Login.propTypes = {
  loginUser: PropTypes.func.isRequired,
  userProfile: PropTypes.shape({}),
  isLoggingIn: PropTypes.bool,
  loginError: PropTypes.node,
};

Login.defaultProps = {
  userProfile: undefined,
  isLoggingIn: false,
  loginError: undefined,
};

const mapStateToProps = (state) => ({
  userProfile: state.user.profile,
  isLoggingIn: state.user.isLoggingIn,
  loginError: state.user.loginError,
});

const mapDispatch = (dispatch) => bindActionCreators({
  loginUser: loginUserAction,
}, dispatch);

export default connect(mapStateToProps, mapDispatch)(Login);
