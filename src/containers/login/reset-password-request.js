import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';

import { requestPasswordReset } from 'services';
import 'actions/user';
import CloseOutlined from 'icons/CloseOutlined';
import {
  Root,
  StyledH1,
  StyledH2,
  StyledForm,
  StyledInput,
  FormMessage,
} from 'styles/login';
import { StyledButton, StyledText } from 'styles/app';
import styled from 'styled-components';

const HeaderText = styled(StyledH2)`
  height: 32px;
  height: 2rem;
`;

const ResetPasswordText = styled(StyledText)`
  margin-bottom: 32px;
  margin-bottom: 2rem;
  display: inline-block;
`;

const ThankYouText = styled(StyledText)`
  margin-top: 24px;
  margin-top: 1.5rem;
  display: inline-block;
`;

const SubmitButton = styled(StyledButton)`
  margin-top: -16px;
  margin-top: -1rem;
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
      <StyledForm className={thanks ? 'thanks' : ''} onSubmit={onResetClicked}>
        {!thanks ? (
          <>
            <HeaderText>RESET YOUR PASSWORD</HeaderText>
            <ResetPasswordText
              size="large"
              color="gray"
            >
              Enter your email address and we will
              <br />
              send you a link to reset your password
            </ResetPasswordText>
            <StyledInput placeholder="email" onChange={onEmailChanged} />
            <FormMessage size="large">
              {error && <StyledText size="small" color="pink">email address</StyledText>}
            </FormMessage>
            <SubmitButton
              htmlType="submit"
              color="blue"
              width={144}
              role="button"
              tabIndex={0}
              onClick={onResetClicked}
              loading={loading}
            >
              Submit
            </SubmitButton>
          </>
        ) : (
          <>
            <Link to="/login"><CloseOutlined color="gray" /></Link>
            <StyledH2>HELP IS ON THE WAY</StyledH2>
            <ThankYouText
              size="large"
              color="gray"
            >
              Please check your email to reset your password.
            </ThankYouText>
          </>
        )}
      </StyledForm>
    </Root>
  );
};

ResetPasswordRequest.propTypes = {
  error: PropTypes.bool,
  thanks: PropTypes.bool,
};

ResetPasswordRequest.defaultProps = {
  error: false,
  thanks: false,
};

export default ResetPasswordRequest;
