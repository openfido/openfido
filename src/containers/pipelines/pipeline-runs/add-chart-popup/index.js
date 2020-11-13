import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import { chartTypes } from 'config/charts';
import { addChart } from 'actions/charts';
import CloseOutlined from 'icons/CloseOutlined';
import { StyledModal } from 'styles/app';
import colors from 'styles/colors';
import SelectArtifactStep from './select-artifact-step';
import AddImageStep from './add-image-step';
import SelectChartTypeStep from './select-chart-type-step';
import ConfigChartStep from './config-chart-step';

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
    padding: 20px 32px 24px 36px;
    border-radius: 3px;
    background-color: ${colors.lightBg};
    min-height: 404px;
  }
  input {
    width: 272px;
  }
  img {
    max-height: 364px;
  }
  form {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 360px;
  }
`;

const AddChartPopup = ({
  handleOk, handleCancel, pipeline_uuid, pipeline_run_uuid, artifacts,
}) => {
  const [step, setStep] = useState(1);
  const [selectedArtifact, setSelectedArtifact] = useState(null);
  const [chartType, setChartType] = useState(null);

  const currentOrg = useSelector((state) => state.user.currentOrg);
  const dispatch = useDispatch();

  const isImage = selectedArtifact && selectedArtifact.name && selectedArtifact.name.match(/\.(png|svg|gif|jpe?g|tiff|bmp)$/i);

  const onAddChartClicked = (title, chartConfig = null) => {
    if (selectedArtifact && chartType) {
      dispatch(
        addChart(currentOrg, pipeline_uuid, pipeline_run_uuid, title, selectedArtifact && selectedArtifact.uuid, chartType, chartConfig),
      );
    }

    handleOk();
  };

  const onArtifactSelected = () => {
    if (selectedArtifact) {
      setStep(2);

      if (isImage) {
        setChartType(chartTypes.IMAGE_CHART);
      }
    }
  };

  const onChartTypeSelected = () => {
    if (chartType) {
      setStep(3);
    }
  };

  return (
    <Modal
      visible
      footer={null}
      onOk={handleOk}
      onCancel={handleCancel}
      closeIcon={<CloseOutlined color="darkText" />}
      width={690}
      maskStyle={{ position: 'absolute', top: '82px', left: '250px' }}
      style={{ position: 'absolute', top: '179px', left: 'calc(((100vw - 690px + 250px) / 2))' }}
      title={step === 2 && isImage ? 'Add an Image' : 'Add a Chart'}
    >
      {step === 1 && (
        <SelectArtifactStep
          artifacts={artifacts}
          selectedArtifact={selectedArtifact}
          setSelectedArtifact={setSelectedArtifact}
          onNextClicked={onArtifactSelected}
        />
      )}
      {step === 2 && isImage && (
        <AddImageStep
          selectedArtifact={selectedArtifact}
          onNextClicked={onAddChartClicked}
        />
      )}
      {step === 2 && !isImage && (
        <SelectChartTypeStep
          chartType={chartType}
          setChartType={setChartType}
          onNextClicked={onChartTypeSelected}
        />
      )}
      {step === 3 && !isImage && (
        <ConfigChartStep
          selectedArtifact={selectedArtifact}
          chartType={chartType}
          onNextClicked={onAddChartClicked}
        />
      )}
    </Modal>
  );
};

AddChartPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
  pipeline_uuid: PropTypes.string.isRequired,
  pipeline_run_uuid: PropTypes.string.isRequired,
  artifacts: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
    uuid: PropTypes.string.isRequired,
  })).isRequired,
};

export default AddChartPopup;
