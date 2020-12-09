import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useSelector, useDispatch } from 'react-redux';
import styled from 'styled-components';
import {
  requestUpdatePipelineRunChart,
} from 'services';
import { updateChart } from 'actions/charts';
import { StyledText, StyledInput, StyledButton } from 'styles/app';
import EditOutlined from 'icons/EditOutlined';
import DeleteOutlined from 'icons/DeleteOutlined';
import colors from 'styles/colors';
import DeleteChartPopUp from './delete-chart-popup';

const StyledForm = styled.form`
  display: grid;
  align-items: flex-start;
  grid-gap: 16px;
  grid-gap: 1rem;
  max-width: inherit;
  label {
    position: relative;
    cursor: pointer;
    &:hover {
      svg path {
        fill: ${colors.blue};
      }
      .anticon-delete-outlined svg path {
        fill: ${colors.pink};
      }
    }
    button {
      margin-top: 8px;
      margin-top: 0.5rem;
    }
  }
  .anticon {
    top: auto;
    bottom: 16px;
    bottom: 1rem;
    right: 16px;
    right: 1rem;
    &.anticon-delete-outlined {
      right: -32px;
      right: -2rem;
      bottom: 48px;
      bottom: 3rem;
    }
  }
  input {
    &.unfocusable {
      pointer-events: none;
    }
  }
`;

const FormMessage = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const EditChart = ({ chart, pipelineUuid, pipelineRun }) => {
  const currentOrg = useSelector((state) => state.user.currentOrg);

  const [selectedChart, setSelectedChart] = useState(null);
  const [selectedChartName, setSelectedChartName] = useState(null);
  const [selectedInput, setSelectedInput] = useState(null);
  const [showDeletePopup, setShowDeletePopup] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const dispatch = useDispatch();

  const onChartNameClick = (e, chartUuid, chartName) => {
    setError(null);
    setLoading(false);
    setSelectedChart(chartUuid);
    setSelectedChartName(chartName);
    setSelectedInput(e.target);
  };

  const setChartName = (e) => {
    setSelectedChartName(e.target.value);
  };

  const onSaveClicked = (e) => {
    e.preventDefault();

    if (!loading) {
      setLoading(true);

      requestUpdatePipelineRunChart(
        currentOrg,
        pipelineUuid,
        pipelineRun.uuid,
        chart.uuid,
        { name: selectedChartName },
      )
        .then(() => {
          setChartName({
            target: {
              value: selectedChartName,
            },
          });
          setError(null);
          setLoading(false);
          if (selectedInput) selectedInput.blur();
          dispatch(
            updateChart(
              currentOrg,
              pipelineUuid,
              pipelineRun.uuid,
              chart.uuid,
              selectedChartName,
            ),
          );
        })
        .catch(() => {
          setError('save');
          setLoading(false);
        });
    }
  };

  const onPermanentlyDeleteClicked = () => {
    setSelectedChart(null);
    setSelectedChartName(null);
    setError(null);
    setLoading(false);
    setSelectedInput(null);

    setShowDeletePopup(false);
  };

  const openDeletePopup = (e) => {
    e.preventDefault();
    setShowDeletePopup(true);
  };

  const closeDeletePopup = () => {
    setShowDeletePopup(false);
  };
  return (
    <>
      <StyledForm onSubmit={onSaveClicked} autoComplete="off" onClick={(e) => e.stopPropagation()}>
        <label
          aria-label="Edit Chart edit label"
          key={chart.uuid}
          htmlFor={chart.uuid}
        >
          <StyledInput
            aria-label="Edit Chart edit input"
            type="text"
            bgcolor="white"
            size="large"
            className={chart.uuid === selectedChart ? '' : ' unfocusable'}
            name={chart.uuid}
            id={chart.uuid}
            value={chart.uuid === selectedChart ? selectedChartName : chart.name}
            tabIndex={-1}
            onChange={setChartName}
            onClick={(e) => onChartNameClick(e, chart.uuid, chart.name)}
          />
          {chart.uuid !== selectedChart && <EditOutlined />}
          {chart.uuid === selectedChart && <DeleteOutlined onClick={(e) => openDeletePopup(e, chart.name)} />}
          {chart.uuid === selectedChart && (
          <FormMessage>
            <StyledText color="pink">
              {error === 'save' && 'Could not save chart name.'}
              {error === 'delete' && 'Could not delete chart.'}
            </StyledText>
            <StyledButton
              htmlType="submit"
              color="lightBlue"
              hoverbgcolor="blue"
              width={50}
              onClick={onSaveClicked}
            >
              <span>Save</span>
            </StyledButton>
          </FormMessage>
          )}
        </label>
      </StyledForm>
      {showDeletePopup && selectedChart && (
        <DeleteChartPopUp
          handleOk={onPermanentlyDeleteClicked}
          handleCancel={closeDeletePopup}
          organizationUUID={currentOrg}
          pipelineUuid={pipelineUuid}
          pipelineRunUuid={pipelineRun.uuid}
          chartName={selectedChartName}
          chartUuid={chart.uuid}
        />
      )}
    </>
  );
};

EditChart.propTypes = {
  chart: PropTypes.objectOf(PropTypes.any).isRequired,
  pipelineUuid: PropTypes.string.isRequired,
  pipelineRun: PropTypes.objectOf(PropTypes.any).isRequired,
};

export default EditChart;
