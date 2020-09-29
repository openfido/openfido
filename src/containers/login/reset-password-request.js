import React, { useState } from 'react';
import styled from 'styled-components';

import { requestPasswordReset } from 'services';
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
`;

const ResetPasswordText = styled(StyledText)`
  margin-bottom: 40px;
  margin-bottom: 2.5rem;
  display: inline-block;
`;

const ThankYouText = styled(StyledText)`
  margin-top: 40px;
  margin-top: 2.5rem;
  display: inline-block;
`;

const ErrorText = styled(StyledText)`
  color: ${colors.pink};
  padding: 0.75rem 0;
  height: 2.5rem;
  margin-bottom: 20px;
  margin-bottom: 1.25rem;
`;

const FormMessage = styled.div`
  padding: 0.75rem 0;
  height: 2.5rem;
  margin-bottom: 20px;
  margin-bottom: 1.25rem;
`;

const Root = styled.div`
  width: 100%;
  height: 100vh;
  text-align: center;
`;

const ResetPasswordRequest = ({ error: defaultError, thanks: defaultThanks }) => {
  const [email, setEmail] = useState();
  const [thanks, setThanks] = useState(defaultThanks);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(defaultError);

  const onEmailChanged = (e) => {
    setEmail(e.target.value);
  };

  const onResetClicked = (e) => {
    e.preventDefault();
    requestPasswordReset(email)
      .then(() => {
        setThanks(true);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  };

  return (
    <Root>
      <StyledH1>
        Welcome to
        <br />
        OpenFIDO
      </StyledH1>
      <StyledForm onSubmit={onResetClicked}>
        <StyledH2>{!thanks ? 'Reset Your Password' : 'Help is on the Way'}</StyledH2>
        {!thanks && (
        <ResetPasswordText
          size="large"
          color="gray"
        >
          Enter your email address and we will send you a link to reset your password
        </ResetPasswordText>
        )}
        {thanks && (
        <ThankYouText
          size="large"
          color="gray"
        >
          Please check your email to reset your password.
        </ThankYouText>
        )}
        {!thanks && <StyledInput type="email" placeholder="EMAIL" onChange={onEmailChanged} />}
        {!thanks && <FormMessage>
          {error && (
          <ErrorText
            size="middle"
            color="gray"
          >
            email address
          </ErrorText>
          )}
        </FormMessage>}
        {!thanks && <StyledButton
          color="blue"
          width="144"
          role="button"
          tabIndex={0}
          onClick={onResetClicked}
          loading={loading}
        >
          Submit
        </StyledButton>}
      </StyledForm>
    </Root>
  );
};

export default ResetPasswordRequest;
