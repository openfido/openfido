import React, { useState } from "react";
import PropTypes from "prop-types";
import { useSelector } from "react-redux";
import styled from "styled-components";
import { Space } from "antd";

import { requestDeletePipelineRun } from "services";
import CloseOutlined from "icons/CloseOutlined";
import AlertOutlined from "icons/AlertOutlined";
import { 
  StyledH2, 
  StyledModal, 
  StyledButton, 
  StyledText } from "styles/app";

const Modal = styled(StyledModal)`
  h2 {
    line-height: 48px;
    line-height: 3rem;
    position: relative;
    .anticon {
      right: auto;
      top: 16px;
      top: 1rem;
      margin-left: 8px;
      margin-left: 0.5rem;
    }
    p {
      text-align: center;
      line-height: 32px;
      line-height: 2rem;
    }
    margin-bottom: 0;
  }
  .anticon-close-outlined {
    top: 18px;
    right: 18px;
  }
  .ant-modal-body {
    padding: 24px 48px 48px 36px;
    border-radius: 3px;
  }
`;

const DeletePipelineRunPopup = ({
  handleCancel,
  pipelineUUID,
  pipelineName,
  pipelineRunUUID,
  pipelineRunNumber,
  handleOk,
}) => {
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const [loading, setLoading] = useState(false);

  const deletePipelineRun = () => {
    if (!loading) {
      setLoading(true);
      requestDeletePipelineRun(currentOrg, pipelineUUID, pipelineRunUUID)
        .then(() => {
          handleOk();
        })
        .catch(() => {
          setLoading(false);
        });
    }
  };

  return (
      <Modal
        visible
        footer={null}
        mask={false}
        onOk={handleOk}
        onCancel={handleCancel}
        closeIcon={<CloseOutlined />}
        width={390}
      >
        {
          <>
            <StyledH2 color="pink">
              <StyledText color="pink">
                ALERT
                <AlertOutlined />
              </StyledText>
            </StyledH2>
            <Space direction="vertical" size={36} align="center">
              <StyledText color="gray" size="large">
                You are about to delete
                <br />
                <StyledText color="pink">
                  Pipeline Run #{pipelineRunNumber} of {pipelineName}
                </StyledText>
                <br /> <strong>This action cannot be undone.</strong> Please be
                certain.
              </StyledText>
              <StyledButton
                size="middle"
                color="blue"
                width={108}
                onClick={handleCancel}
              >
                <div>
                  DO NOT
                  <br />
                  DELETE
                </div>
              </StyledButton>
              <StyledButton
                type="text"
                color="transparent"
                onClick={deletePipelineRun}
              >
                <StyledText
                  size="large"
                  fontweight={500}
                  align="center"
                  display="block"
                  color="pink"
                >
                  Yes, I am certain that
                  <br />I want to delete
                </StyledText>
              </StyledButton>
            </Space>
          </>
        }
      </Modal>

  );
};

DeletePipelineRunPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
  pipelineUUID: PropTypes.string.isRequired,
  pipelineName: PropTypes.string.isRequired,
  pipelineRunUUID: PropTypes.string.isRequired,
  pipelineRunNumber: PropTypes.number.isRequired,
};

export default DeletePipelineRunPopup;
