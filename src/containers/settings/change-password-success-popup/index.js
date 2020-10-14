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
    padding: 28px 32px 48px 32px;
    border-radius: 3px;
  }
  .ant-modal-content {
    box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.05);
  }
  button {
    margin: 0 auto;
  }
`;

const ChangePasswordSuccessPopup = ({ handleOk, handleCancel }) => (
  <Modal
    visible
    footer={null}
    onOk={handleOk}
    onCancel={handleCancel}
    closeIcon={<CloseOutlined />}
    width={390}
  >
    <StyledH2>
      SUCCESS!
    </StyledH2>
    <Space direction="vertical" size={56} align="center">
      <StyledText size="large" color="gray">
        You have successfully changed your password.
      </StyledText>
      <StyledButton
        size="middle"
        color="blue"
        onClick={handleOk}
        width={108}
        style={{ padding: 0 }}
      >
        <label>
          RETURN TO
          <br />
          SETTINGS
        </label>
      </StyledButton>
    </Space>
  </Modal>
);

ChangePasswordSuccessPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
};

export default ChangePasswordSuccessPopup;
