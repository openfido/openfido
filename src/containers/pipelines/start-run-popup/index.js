import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

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
  padding: 0 42px 28px 36px;
  padding: 0 2.625rem 1.75rem 2.25rem;
  border-bottom: 1px solid ${colors.grey};
`;

const ArtifactsSection = styled.div`
  padding: 24px 36px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-row-gap: 24px;
  grid-row-gap: 1.5rem;
  grid-column-gap: 88px;
  grid-column-gap: 5.5
`;

export const Artifact = styled.div`
  background-color ${colors.white};
  color: ${colors.black};
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px 14px 24px;
  font-size: 16px;
  line-height: 19px;
  width: 261px;
  max-height: 64px;
  cursor: pointer;
  position: relative;
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

const StartRunPopup = ({ handleOk, handleCancel }) => (
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
    <StyledForm>
      <UploadSection>
        <UploadBox>
          <input type="file" id="inputs" />
          <CloudOutlined />
          <div>
            <StyledText size="large" color="darkText">
              Drag and drop your input file here, or
              {' '}
              <StyledButton
                type="text"
                size="middle"
                fontweight="bold"
                textcolor="lightBlue"
              >
                <label htmlFor="inputs">
                  browse
                </label>
              </StyledButton>
              .
            </StyledText>
          </div>
        </UploadBox>
      </UploadSection>
      <ArtifactsSection>
        <Artifact>
          CA-Bakersfield-meadows-field-highwind-mocked.tmy3
          <CloseOutlined color="lightGray" />
        </Artifact>
        <Artifact>
          anticipation-ieee123-pole-vulnerability.glm
          <CloseOutlined color="lightGray" />
        </Artifact>
        <Artifact>
          config.json
          <CloseOutlined color="lightGray" />
        </Artifact>
      </ArtifactsSection>
      <StyledButton
        size="middle"
        color="blue"
        width={108}
      >
        Start Run
      </StyledButton>
    </StyledForm>
  </Modal>
);

StartRunPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
};

export default StartRunPopup;
