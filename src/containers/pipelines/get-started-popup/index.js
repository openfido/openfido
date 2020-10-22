import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { Space } from 'antd';

import {
  StyledH2,
  StyledButton,
} from 'styles/app';
import colors from 'styles/colors';

const Popup = styled.div`
  box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.05);
  border-radius: 3px;
  background-color: ${colors.white};
  width: 390px;
  margin: 0 auto;
  height: 365px;
  display: flex;
  align-items: center;
  margin-top: 100px;
  h2 {
    margin-bottom: 0;
  }
`;

const GetStartedPopup = ({ handleOk }) => (
  <Popup>
    <Space direction="vertical" align="center" size={42}>
      <StyledH2 color="gray">
        Create Your First Pipeline
      </StyledH2>
      <StyledButton color="blue" size="middle" width={108} onClick={handleOk}>Get Started</StyledButton>
    </Space>
  </Popup>
);

GetStartedPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
};

export default GetStartedPopup;
