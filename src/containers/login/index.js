import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import styled from 'styled-components';

import { loginUser as loginUserAction } from 'actions/user';
import PropTypes from 'prop-types';

import { ROUTE_PIPELINES, ROUTE_FORGOT_PASSWORD } from 'config/routes';
import colors from 'styles/colors';

import { StyledButton } from 'styles/app';

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
  background-color: #fff;
  text-align: left;
`;

const StyledInput = styled.input`
  width: 330px;
  font-size: 18px;
  font-size: 1.125rem;
  color: #707070;
  border: none;
  padding-bottom: 0.625rem;
  padding-left: 0.25rem;
  padding-right: 0.25rem;
  border-bottom: 1px solid #D2D2D2;
  &::placeholder {
    color: #D2D2D2;
  }
  &:first-child {
    margin-bottom: 20px;
  }
`;

const ForgotPasswordLink = styled.div`
  position: relative;
  a {
    position: absolute;
    top: -0.625rem;
    right: 0;
    font-size: 14px;
    font-size: 0.875rem;
    line-height: 16px;
    line-height: 1rem;
    color: ${colors.gray80};
  }
`;

const ErrorMessage = styled.div`
  font-size: 14px;
  color: ${colors.pink};
`;

const Root = styled.div`
    width: 100%;
    height: 100vh;
    text-align: center;
`;

class Login extends Component {
  constructor() {
    super();
    this.onEmailChanged = this.onEmailChanged.bind(this);
    this.onPasswordChanged = this.onPasswordChanged.bind(this);
    this.onLoginClicked = this.onLoginClicked.bind(this);
    this.state = {
      email: null,
      password: null,
    };
  }

  componentDidUpdate() {
    const { userProfile, history } = this.props;
    if (userProfile) {
      history.push(ROUTE_PIPELINES);
    }
  }

  onEmailChanged(e) {
    this.setState({ email: e.target.value });
  }

  onPasswordChanged(e) {
    this.setState({ password: e.target.value });
  }

  onLoginClicked() {
    const { email, password } = this.state;
    const { loginUser, isLoggingIn } = this.props;

    if (!isLoggingIn) {
      loginUser(email, password);
    }
  }

  render() {
    const { loginError } = this.props;

    return (
      <Root>
        <StyledH1>
          Welcome to
          <br />
          OpenFIDO
        </StyledH1>
        <StyledForm>
          <StyledH2>Sign In</StyledH2>
          <div>
            <StyledInput placeholder="EMAIL" onChange={this.onEmailChanged} />
          </div>
          <div>
            <StyledInput type="password" placeholder="PASSWORD" onChange={this.onPasswordChanged} />
          </div>
          <ForgotPasswordLink>
            <Link to={ROUTE_FORGOT_PASSWORD}>Forgot Password</Link>
          </ForgotPasswordLink>
          <ErrorMessage>
            {loginError && `Invalid credentials entered.`}
          </ErrorMessage>
          <StyledButton
            color="blue"
            width="108"
            role="button"
            tabIndex={0}
            onClick={this.onLoginClicked}
            onKeyPress={this.onLoginClicked}
          >
            Sign In
          </StyledButton>
        </StyledForm>
      </Root>
    );
  }
}

Login.propTypes = {
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
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

export default withRouter(connect(mapStateToProps, mapDispatch)(Login));
