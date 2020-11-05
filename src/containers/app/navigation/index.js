import React from 'react';
import styled from 'styled-components';

import colors from 'styles/colors';
import Profile from './profile';
import Menu from './menu';

const StyledHelpLink = styled.a`
  position: absolute;
  left: 20px;
  bottom: 20px;
  font-size: 16px;
  color: ${colors.blue};
  cursor: pointer;
`;

export default () => (
  <>
    <Profile />
    <Menu />
    <StyledHelpLink href="http://docs.openfido.org.s3-website-us-east-1.amazonaws.com/ " target="_blank">Help</StyledHelpLink>
  </>
);
