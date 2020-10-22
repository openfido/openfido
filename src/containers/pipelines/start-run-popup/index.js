import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useSelector } from 'react-redux';
import styled from 'styled-components';

import { requestStartPipelineRun } from 'services';
import CloseOutlined from 'icons/CloseOutlined';
import CloudOutlined from 'icons/CloudOutlined';
import {
  StyledModal,
  StyledButton,
  StyledText,
} from 'styles/app';
import colors from 'styles/colors';

const Modal = styled(StyledModal)`
  h2 {
    text-transform: uppercase;
    color: ${colors.black};
    text-align: center;
    line-height: 32px;
    line-height: 2rem;
    margin-bottom: 32px;
  }
  .anticon-close-outlined {
    top: 8px;
    right: 12px;
  }
  .ant-modal-body {
    padding: 24px 0;
    border-radius: 6px;
    background-color: ${colors.lightBg};
  }
`;

const StyledForm = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  input[type="file"] {
    display: none;
  }
`;

const UploadBox = styled.div`
  border: 2px dashed ${colors.gray};
  border-radius: 3px;
  position: relative;
  margin-left: 1px;
  &:after {
    content: '';
    position: absolute;
    left: -1px;
    top: -1px;
    right: -1px;
    bottom: -1px;
    border: 1px solid ${colors.lightBg};
    pointer-events: none;
  }
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  height: 169px;
  padding: 8px 20px 20px 20px;
  .anticon {
    position: static;
  }
  .ant-btn label {
    padding: 0;
  }
`;

export const UploadSection = styled.div`
  width: 100%;
  padding: 0 42px 16px 36px;
  padding: 0 2.625rem 1.75rem 2.25rem;
  border-bottom: 1px solid ${colors.grey};
`;

const ArtifactsSection = styled.div`
  padding: 24px 36px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 48px;
  grid-row-gap: 24px;
  grid-row-gap: 1.5rem;
  grid-column-gap: 88px;
  grid-column-gap: 5.5rem;
  overflow-y: scroll;
  height: 188px;
  margin-bottom: 24px;
  margin-bottom: 1.5rem;
`;

export const Artifact = styled.div`
  background-color ${colors.white};
  color: ${colors.black};
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 16px 4px 24px;
  padding: 0.25rem 1rem 0.25rem 1.5rem;
  font-size: 16px;
  line-height: 19px;
  width: 261px;
  height: 48px;
  max-height: 48px;
  cursor: pointer;
  position: relative;
  span:first-child {
    margin-right: 8px;
    margin-right: 0.5rem;
    white-space: pre;
    overflow: hidden;
  }
  .anticon {
    position: static;
    float: right;
    svg {
      width: 18px;
      width: 1.125rem;
      height: 18px;
      height: 1.125rem;
    }
  }
  &:hover {
    .anticon svg line {
      stroke: ${colors.gray20};
    }
  }
`;

const StartRunPopup = ({ handleOk, handleCancel, pipeline_uuid }) => {
  const currentOrg = useSelector((state) => state.user.currentOrg);

  const [inputs, setInputs] = useState([]);

  const onInputsChanged = (e) => {
    const inputFiles = [];

    Array.from(e.target.files).forEach((file) => {
      inputFiles.push(file);
    });

    setInputs([
      ...inputs,
      ...inputFiles,
    ]);
  };

  const onStartRunClicked = () => {
    requestStartPipelineRun(currentOrg, pipeline_uuid, inputs)
      .then(() => {
        handleOk();
      });
  };

  const removeInputFile = (index) => {
    const inputFiles = [...inputs];
    inputFiles.splice(index, 1);
    setInputs(inputFiles);
  };

  return (
    <Modal
      visible
      footer={null}
      onOk={handleOk}
      onCancel={handleCancel}
      closeIcon={<CloseOutlined color="darkText" />}
      width={690}
      maskStyle={{ top: '82px', left: '250px' }}
      style={{ position: 'fixed', top: '179px', left: 'calc(((100vw - 690px + 250px) / 2))' }}
      title="Start a run"
    >
      <StyledForm onSubmit={onStartRunClicked}>
        <UploadSection>
          <UploadBox>
            <input type="file" id="inputs" onChange={onInputsChanged} multiple />
            <CloudOutlined />
            <div>
              <StyledText size="large" color="darkText">
                Drag and drop your input file here, or
                {' '}
                <StyledButton
                  type="text"
                  size="middle"
                  textcolor="lightBlue"
                >
                  <label htmlFor="inputs">
                    <strong>browse</strong>
                  </label>
                </StyledButton>
                .
              </StyledText>
            </div>
          </UploadBox>
        </UploadSection>
        <ArtifactsSection>
          {inputs && Array.from(inputs).map((inputFile, index) => (
            <Artifact key={`${inputFile.name}${Math.random()}`} alt={inputFile.name}>
              <StyledText>{inputFile.name}</StyledText>
              <CloseOutlined color="lightGray" onClick={() => removeInputFile(index)} />
            </Artifact>
          ))}
        </ArtifactsSection>
        <StyledButton
          size="middle"
          color="blue"
          width={108}
          onClick={onStartRunClicked}
        >
          Start Run
        </StyledButton>
      </StyledForm>
    </Modal>
  );
};

StartRunPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
  pipeline_uuid: PropTypes.string.isRequired,
};

export default StartRunPopup;
