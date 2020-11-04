import React, { useState } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import CloseOutlined from 'icons/CloseOutlined';
import {
  StyledH4,
  StyledInput,
  StyledModal,
  StyledButton, StyledText,
} from 'styles/app';
import colors from 'styles/colors';
import LinesImg from './images/lines.png';
import MapImg from './images/map.png';

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
    top: 18px;
    right: 18px;
  }
  .ant-modal-body {
    padding: 20px 32px 24px 36px;
    border-radius: 3px;
    background-color: ${colors.lightBg};
    min-height: 404px;
    display: flex;
    justify-content: space-between;
  }
  input {
    width: 272px;
  }
  img {
    max-height: 364px;
  }
`;

const ArtifactsList = styled.ul`
  list-style-type: none;
  padding: 0;
  margin: 12px 0;
  margin: 0.75rem 0;
  li {
    background-color: ${colors.white};
    &:not(:last-child) {
      border-bottom: 1px solid ${colors.lightGray};
    }
    button.ant-btn {
      display: block;
      padding: 16px 22px;
      padding: 1rem 1.375rem;
      font-weight: 400;
      width: 100%;
      text-align: left;
      border-radius: 0;
      transition: none;
      &:active, &:focus {
        border-left: 5px solid ${colors.blue};
        background-color: ${colors.lightActiveHover};
        padding-left: 17px;
        padding-left: 1.0625rem;
      }
    }
  }
`;

const ChartTypesList = styled.ul`
  list-style-type: none;
  padding: 0;
  margin: 12px 0;
  margin: 0.75rem 0;
  display: flex;
  justify-content: space-between;
  li {
   button.ant-btn {
     width: 178px;
     height: 178px;
     padding: 28px 8px;
     padding: 1.75rem 0.5rem;
     flex-wrap: wrap;
     border: 3px solid ${colors.white};
     border-radius: 2px;
     &, &:hover {
       background-color: ${colors.white};
     }
     &:active, &:focus {
       border: 3px solid ${colors.lightBlue};
       background-color: ${colors.white};
     }
   }
  }
`;

const PopupButton = styled(StyledButton)`
  margin: 20px auto 0 auto;
  margin: 1.25rem auto 0 auto;
`;

const AxisItem = styled.div`
  background-color ${colors.white};
  color: ${colors.darkText};
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px 4px 12px;
  padding: 0.25rem 0.5rem 0.25rem 0.75rem;
  margin-top: 16px;
  margin-top: 1rem;
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
    text-overflow: ellipsis;
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

const AxesList = styled.div`
  display: flex;
  justify-content: space-between;
`;

const AddChartPopup = ({ handleOk, handleCancel, artifacts }) => {
  const [selectedArtifact, setSelectedArtifact] = useState(null);
  const [step, setStep] = useState(1);

  const isImage = selectedArtifact && selectedArtifact.name && selectedArtifact.name.match(/\.(png|svg|gif|jpe?g|tiff|bmp)$/i);

  const onAddChartClicked = () => {
    handleOk();
  };

  const onXAxisRemoveClicked = () => {

  };

  const selectArtifact = (
    <>
      <div>
        <StyledH4 color="darkText">Select an artifact</StyledH4>
        <ArtifactsList>
          {artifacts && artifacts.map((artifact) => (
            <li>
              <StyledButton
                type="text"
                size="large"
                textcolor="lightBlue"
                onClick={() => setSelectedArtifact(artifact)}
              >
                {artifact.name}
              </StyledButton>
            </li>
          ))}
        </ArtifactsList>
      </div>
      <PopupButton size="middle" color="blue" width={108} onClick={() => setStep(2)}>
        Next
      </PopupButton>
    </>
  );

  const selectChartType = (
    <>
      <StyledH4 color="darkText">Select an artifact</StyledH4>
      <ChartTypesList>
        <li>
          <StyledButton type="text" size="middle" textcolor="darkText">
            Line Chart
            <img src={LinesImg} alt="Line" />
          </StyledButton>
        </li>
        <li>
          <StyledButton type="text" size="middle" textcolor="darkText">
            Bar Chart
          </StyledButton>
        </li>
        <li>
          <StyledButton type="text" size="middle" textcolor="darkText">
            Map Chart
            <img src={MapImg} alt="Map" />
          </StyledButton>
        </li>
      </ChartTypesList>
      <PopupButton size="middle" color="blue" width={108} onClick={() => setStep(3)}>
        Next
      </PopupButton>
    </>
  );

  const addImage = (
    <>
      <StyledInput size="middle" placeholder="Edit Name of Image" bgcolor="white" />
      {selectedArtifact && selectedArtifact.url && (
        <img src={selectedArtifact.url} alt={selectedArtifact.name} />
      )}
      <PopupButton size="middle" color="blue" width={108} onClick={onAddChartClicked}>
        Add Chart
      </PopupButton>
    </>
  );

  const addChart = (
    <>
      <StyledInput size="middle" placeholder="Edit Name of Chart" bgcolor="white" />
      <section>
        graph
      </section>
      <AxesList>
        <div>
          <strong>
            X-axis
          </strong>
          <AxisItem title="DateTime">
            <StyledText>DateTime</StyledText>
            <CloseOutlined color="lightGray" onClick={() => onXAxisRemoveClicked()} />
          </AxisItem>
        </div>
        <div>
          <strong>
            Y-axis
          </strong>
          <AxisItem title="DateTime">
            <StyledText>L1</StyledText>
            <CloseOutlined color="lightGray" onClick={() => onXAxisRemoveClicked()} />
          </AxisItem>
          <AxisItem title="DateTime">
            <StyledText>L2</StyledText>
            <CloseOutlined color="lightGray" onClick={() => onXAxisRemoveClicked()} />
          </AxisItem>
        </div>
      </AxesList>
      <PopupButton size="middle" color="blue" width={108} onClick={onAddChartClicked}>
        Add Chart
      </PopupButton>
    </>
  );

  return (
    <Modal
      visible
      footer={null}
      onOk={handleOk}
      onCancel={handleCancel}
      closeIcon={<CloseOutlined />}
      width={690}
      maskStyle={{ top: '82px', left: '250px' }}
      style={{ position: 'fixed', top: '179px', left: 'calc(((100vw - 690px + 250px) / 2))' }}
      title={step === 2 && isImage ? 'Add an Image' : 'Add a Chart'}
    >
      {step === 1 && selectArtifact}
      {step === 2 && isImage && addImage}
      {step === 2 && !isImage && selectChartType}
      {step === 3 && !isImage && addChart}
    </Modal>
  );
};

AddChartPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
  artifacts: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default AddChartPopup;
