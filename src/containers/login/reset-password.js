import React from 'react';
import styled from 'styled-components';

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
  &:first-of-type {
    margin-bottom: 32px;
    margin-bottom: 2rem;
  }
`;

const ResetPasswordText = styled(StyledText)`
  margin-bottom: 40px;
  margin-bottom: 2.5rem;
  display: inline-block;
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

const ResetPassword = () => (
  <Root>
    <StyledH1>
      Welcome to
      <br />
      OpenFIDO
    </StyledH1>
    <StyledForm>
      <StyledH2>Reset Your Password</StyledH2>
      <ResetPasswordText
        size="large"
        color="gray"
      >
        Enter your email address and we will send you a link to reset your password
      </ResetPasswordText>
      <StyledInput placeholder="EMAIL" />
      {/* <ErrorMessage>
                    Invalid credentials entered.
                </ErrorMessage> */}
      <StyledButton
        color="blue"
        width="144"
        role="button"
        tabIndex={0}
      >
        Submit
      </StyledButton>
    </StyledForm>
  </Root>
);

export default ResetPassword;
