import React, { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import { requestUpdatePassword } from 'services';
import 'actions/user';
import { StyledButton, StyledText } from 'styles/app';
import colors from 'styles/colors';

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
  margin-bottom: 16px;
  margin-bottom: 1rem;
  color: ${colors.blue};
  text-transform: uppercase;
`;

const StyledForm = styled.form`
  position: relative;
  width: 390px;
  height: 522px;
  padding: 28px 32px;
  margin: 42px auto 0 auto;
  margin: 2.625rem auto 0 auto;
  background-color: ${colors.white};
  text-align: left;
  border-radius: 3px;
  label span {
    line-height: 2.5rem;
  }
  .anticon {
    top: 16px;
    top: 1rem;
    right: 16px;
    right: 1rem;
    cursor: pointer;
  }
  &.thanks {
    height: 300px;
  }
`;

const StyledInput = styled.input`
  width: 330px;
  font-size: 16px;
  font-size: 1.125rem;
  font-weight: 400;
  color: ${colors.gray};
  padding-bottom: 0.625rem;
  padding-left: 0;
  padding-right: 0;
  border: none;
  border-bottom: 1px solid ${colors.lightGray};
  &::placeholder {
    color: ${colors.darkGray};
  }
  &:first-of-type {
    margin-bottom: 32px;
    margin-bottom: 2rem;
  }
`;

const ThankYouText = styled(StyledText)`
  margin: 40px 0;
  margin: 2.5rem 0;
  display: inline-block;
`;

const FormMessage = styled.div`
  padding: 0.75rem 0;
  height: 2.5rem;
`;

const Root = styled.div`
  width: 100%;
  height: 100vh;
  text-align: center;
`;

const ResetPassword = ({ error: defaultError, thanks: defaultThanks }) => {
  const { reset_token: resetToken, email } = useParams();

  const [password, setPassword] = useState();
  const [confirmPassword, setConfirmPassword] = useState();
  const [thanks, setThanks] = useState(defaultThanks);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(defaultError);
  const [passwordMismatch, setPasswordMismatch] = useState(false);

  const onPasswordChanged = (e) => {
    setPassword(e.target.value);
  };

  const onConfirmPasswordChanged = (e) => {
    setConfirmPassword(e.target.value);
  };

  const onChangePasswordClicked = (e) => {
    e.preventDefault();
    if (password === confirmPassword) {
      requestUpdatePassword(email, resetToken, password)
        .then(() => {
          setThanks(true);
        })
        .catch(() => {
          setError(true);
          setLoading(false);
        });
    } else {
      setPasswordMismatch(true);
      setLoading(false);
      setError(false);
    }
  };

  return (
    <Root>
      <StyledH1>
        Welcome to
        <br />
        OpenFIDO
      </StyledH1>
      <StyledForm className={thanks ? 'thanks' : ''} onSubmit={onChangePasswordClicked}>
        {!thanks ? (
          <>
            <StyledH2>Reset Your Password</StyledH2>
            <label htmlFor="newPassword">
              <StyledText
                size="middle"
                color="gray"
              >
                New Password
              </StyledText>
              <StyledInput type="password" name="newPassword" id="newPassword" placeholder="password" onChange={onPasswordChanged} />
            </label>
            <label htmlFor="confirmPassword">
              <StyledText
                size="middle"
                color="gray"
              >
                Re-Enter Password
              </StyledText>
              <StyledInput type="password" name="confirmPassword" id="confirmPassword" placeholder="password" onChange={onConfirmPasswordChanged} />
            </label>
            <FormMessage>
              {error && (
              <StyledText
                size="middle"
                color="pink"
              >
                Minimum 10 characters
              </StyledText>
              )}
              {passwordMismatch && <StyledText size="middle" color="pink" float="right">Password mismatch</StyledText>}
            </FormMessage>
            <StyledButton
              color="blue"
              width="144"
              role="button"
              tabIndex={0}
              onClick={onChangePasswordClicked}
              loading={loading}
            >
              Submit
            </StyledButton>
          </>
        ) : (
          <>
            <StyledH2>Password has been reset</StyledH2>
            <ThankYouText
              size="large"
              color="gray"
            >
              You have sucessfully changed your password.
            </ThankYouText>
            <Link to="/login">
              <StyledButton
                color="blue"
                width="108"
                height="58"
                role="button"
                tabIndex={0}
              >
                Return to
                <br />
                Sign In
              </StyledButton>
            </Link>
          </>
        )}
      </StyledForm>
    </Root>
  );
};

ResetPassword.propTypes = {
  error: PropTypes.bool,
  thanks: PropTypes.bool,
};

ResetPassword.defaultProps = {
  error: false,
  thanks: false,
};

export default ResetPassword;
