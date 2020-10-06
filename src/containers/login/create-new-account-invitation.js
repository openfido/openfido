import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { createUser } from 'actions/user';
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
  margin-bottom: 0;
  color: ${colors.blue};
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
  button {
    margin-top: 32px;
    margin-top: 2rem;
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
    color: ${colors.lightGray};
  }
  margin-top: 32px;
  margin-top: 2rem;
  &:last-of-type {
    margin-top: 16px;
    margin-top: 1rem;
  }
`;

const FormMessage = styled.div`
  padding-top: 0.25rem;
  font-size: 12px;
  line-height: 14px;
  height: 18px;
  height: 1.125rem;
`;

const Root = styled.div`
  width: 100%;
  height: 100vh;
  text-align: center;
`;

const CreateNewAccountInvitation = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordMismatch, setPasswordMismatch] = useState(false);

  const invitationOrganization = useSelector((state) => state.organization.invitationOrganization);
  const createUserError = useSelector((state) => state.user.createUserError);
  const dispatch = useDispatch();

  const onEmailChanged = (e) => {
    setEmail(e.target.value);
  };

  const onPasswordChanged = (e) => {
    setPassword(e.target.value);
  };

  const onConfirmPasswordChanged = (e) => {
    setConfirmPassword(e.target.value);
  };

  const onSignInClicked = (e) => {
    e.preventDefault();
    if (password === confirmPassword) {
      dispatch(createUser(invitationOrganization, email, password));
      setPasswordMismatch(false);
    } else {
      setPasswordMismatch(true);
    }
  };

  return (
    <Root>
      <StyledH1>
        You've been invited to join
        <br />
        OpenFIDO
      </StyledH1>
      <StyledForm onSubmit={onSignInClicked}>
        <StyledH2>
          Welcome to OpenFIDO.
          <br />
          Please create an account
        </StyledH2>
        <StyledInput type="email" name="email" id="email" placeholder="email" onChange={onEmailChanged} />
        <StyledInput type="password" name="password" id="newPassword" placeholder="password" onChange={onPasswordChanged} />
        <FormMessage>
          {passwordMismatch && <StyledText size="small" color="pink">Passwords do not match</StyledText>}
          <StyledText color={createUserError && password.length < 10 ? 'pink' : 'gray80'} float="right">Minimum 10 characters</StyledText>
        </FormMessage>
        <StyledInput type="password" name="confirmPassword" id="confirmPassword" placeholder="re-enter password" onChange={onConfirmPasswordChanged} />
        <FormMessage>
          {createUserError && password.length >= 10 && password === confirmPassword && !passwordMismatch && (
            <StyledText size="small" color="pink">Could not create account</StyledText>
          )}
        </FormMessage>
        <StyledButton
          htmlType="submit"
          color="blue"
          width={106}
          role="button"
          tabIndex={0}
          onClick={onSignInClicked}
        >
          Sign In
        </StyledButton>
      </StyledForm>
    </Root>
  );
};

export default CreateNewAccountInvitation;
