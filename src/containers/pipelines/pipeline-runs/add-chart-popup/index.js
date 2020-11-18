import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import {
  ALLOWABLE_ARTIFACT_IMAGE_FORMATS,
  CHART_TYPES,
} from 'config/charts';
import { addChart, getCharts, processArtifact } from 'actions/charts';
import CloseOutlined from 'icons/CloseOutlined';
import { StyledModal } from 'styles/app';
import colors from 'styles/colors';
import SelectArtifactStep from './select-artifact-step';
import AddImageStep from './add-image-step';
import SelectChartTypeStep from './select-chart-type-step';
import ConfigChartStep from './config-chart-step';

const NoGraphingOption = styled.div`
  margin: auto;
`;

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
  const chartDatum = useSelector((state) => state.charts.chartDatum);
  const dispatch = useDispatch();

  const isImage = selectedArtifact && selectedArtifact.name && selectedArtifact.name.match(ALLOWABLE_ARTIFACT_IMAGE_FORMATS);

  const onAddChartClicked = (title, chartConfig = null) => {
    if (selectedArtifact && chartType) {
      dispatch(
        addChart(currentOrg, pipeline_uuid, pipeline_run_uuid, title, selectedArtifact && selectedArtifact.uuid, chartType, chartConfig),
      )
        .then(() => {
          dispatch(getCharts(currentOrg, pipeline_uuid, pipeline_run_uuid));
        });
    }

    handleOk();
  };

  const onArtifactSelected = () => {
    if (selectedArtifact) {
      dispatch(processArtifact(selectedArtifact));

      setStep(2);

      if (isImage) {
        setChartType(CHART_TYPES.IMAGE_CHART);
      }
    }
  };

  const onChartTypeSelected = () => {
    if (chartType) {
      setStep(3);
    }
  };

  const chartData = selectedArtifact && selectedArtifact.url in chartDatum && chartDatum[selectedArtifact.url].chartData;
  const chartTypes = selectedArtifact && selectedArtifact.url in chartDatum && chartDatum[selectedArtifact.url].chartTypes;
  const chartScales = selectedArtifact && selectedArtifact.url in chartDatum && chartDatum[selectedArtifact.url].chartScales;

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
      {step === 2 && !isImage && !chartTypes && chartData && (
        <NoGraphingOption>
          <p>No graphing options are available for this file.</p>
          <p>{chartData}</p>
        </NoGraphingOption>
      )}
      {step === 2 && !isImage && chartTypes && (
        <SelectChartTypeStep
          chartType={chartType}
          setChartType={setChartType}
          onNextClicked={onChartTypeSelected}
          chartData={chartData}
          chartTypes={chartTypes}
          chartScales={chartScales}
        />
      )}
      {step === 3 && !isImage && chartData && (
        <ConfigChartStep
          chartType={chartType}
          onNextClicked={onAddChartClicked}
          chartData={chartData}
          chartTypes={chartTypes}
          chartScales={chartScales}
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
