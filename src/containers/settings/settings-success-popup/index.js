import React from 'react';
import PropTypes from 'prop-types';
import { Space } from 'antd';
import styled from 'styled-components';

import CloseOutlined from 'icons/CloseOutlined';
import {
  StyledH2,
  StyledModal,
  StyledButton,
  StyledText,
} from 'styles/app';
import colors from 'styles/colors';

const Modal = styled(StyledModal)`
  h2 {
    color: ${colors.blue};
    line-height: 32px;
    line-height: 2rem;
    margin-bottom: 56px;
    margin-bottom: 3.5rem;
  }
  .anticon {
    top: 18px;
    right: 18px;
    &:hover {
      svg line {
        stroke: ${colors.gray};
      }
    }
  }
  .ant-modal-body {
    padding: 28px 56px 48px 32px;
    border-radius: 3px;
  }
  button {
    margin: 0 auto;
  }
`;

const SettingsSuccessPopup = ({
  handleOk, handleCancel, message, top,
}) => (
  <Modal
    visible
    footer={null}
    mask={false}
    onOk={handleOk}
    onCancel={handleCancel}
    closeIcon={<CloseOutlined />}
    width={390}
    style={{ top }}
  >
    <StyledH2>
      SUCCESS!
    </StyledH2>
    <Space direction="vertical" size={56} align="center">
      <StyledText size="large" color="gray">
        {message}
      </StyledText>
      <StyledButton
        size="middle"
        color="blue"
        onClick={handleOk}
        width={108}
        style={{ padding: 0 }}
      >
        <label>
          Return to
          <br />
          Settings
        </label>
      </StyledButton>
    </Space>
  </Modal>
);

SettingsSuccessPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
  message: PropTypes.string.isRequired,
  top: PropTypes.string,
};

SettingsSuccessPopup.defaultProps = {
  top: '224px',
};

export default SettingsSuccessPopup;
