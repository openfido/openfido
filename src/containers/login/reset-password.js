import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useParams, useHistory } from 'react-router-dom';
import styled from 'styled-components';

import { requestUpdatePassword } from 'services';
import { ROUTE_PIPELINES, ROUTE_LOGIN } from 'config/routes';
import {
  Root,
  StyledH1,
  StyledH2,
  StyledForm,
  StyledInput,
  FormMessage,
} from 'styles/login';
import { StyledButton, StyledText } from 'styles/app';

const HeaderText = styled(StyledH2)`
  height: 24px;
  height: 1.5rem;
`;

const ResetPassword = () => {
  const history = useHistory();
  const { reset_token: resetToken, email } = useParams();

  const [password, setPassword] = useState();
  const [confirmPassword, setConfirmPassword] = useState();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [passwordMismatch, setPasswordMismatch] = useState(false);

  const profile = useSelector((state) => state.user.profile);

  useEffect(() => {
    if (profile) {
      history.push(ROUTE_PIPELINES);
    }
  }, [profile, history]);

  const onPasswordChanged = (e) => {
    setPassword(e.target.value);
  };

  const onConfirmPasswordChanged = (e) => {
    setConfirmPassword(e.target.value);
  };

  const onChangePasswordClicked = (e) => {
    e.preventDefault();

    if (!loading) {
      setLoading(true);

      if (password === confirmPassword) {
        requestUpdatePassword(email, resetToken, password)
          .then(() => {
            history.push(ROUTE_LOGIN);
          })
          .catch(() => {
            setError(true);
            setLoading(false);
            setPasswordMismatch(false);
          });
      } else {
        setPasswordMismatch(true);
        setLoading(false);
        setError(false);
      }
    }
  };

  return (
    <Root>
      <StyledH1>
        Welcome to
        <br />
        OpenFIDO
      </StyledH1>
      <StyledForm onSubmit={onChangePasswordClicked}>
        <HeaderText>RESET YOUR PASSWORD</HeaderText>
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
        <FormMessage size="large">
          <StyledText size="small" color="pink">
            {passwordMismatch && 'Passwords do not match.'}
          </StyledText>
          <StyledText size="small" color={error && !passwordMismatch ? 'pink' : 'gray'}>Minimum 10 characters</StyledText>
        </FormMessage>
        <StyledButton
          htmlType="submit"
          size="middle"
          color="blue"
          width={108}
          role="button"
          tabIndex={0}
          onClick={onChangePasswordClicked}
        >
          Submit
        </StyledButton>
      </StyledForm>
    </Root>
  );
};

export default ResetPassword;
