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
  background-color: #fff;
  text-align: left;
  label {
    line-height: 1.5rem;
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
    margin-bottom: 20px;
    margin-bottom: 1.25rem;
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

const ResetPassword = () => (
  <Root>
    <StyledH1>
      Welcome to
      <br />
      OpenFIDO
    </StyledH1>
    <StyledForm>
      <StyledH2>Reset Your Password</StyledH2>
      <div>
        <label htmlFor="newPassword">
          <StyledText
            size="middle"
            color="gray"
          >
            New Password
          </StyledText>
        </label>
        <StyledInput placeholder="password" />
      </div>
      <div>
        <label htmlFor="confirmPassword">
          <StyledText
            size="middle"
            color="gray"
          >
            Re-Enter Password
          </StyledText>
        </label>
        <StyledInput type="password" placeholder="password" />
      </div>
      <ErrorMessage>
        Minimum 10 characters
      </ErrorMessage>
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
