import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import { getCharts, processArtifact } from 'actions/charts';
import { DATA_VISUALIZATION_TAB } from 'config/pipeline-runs';
import { CHART_TYPES } from 'config/charts';
import { pipelineStates } from 'config/pipeline-status';
import {
  StyledH2,
  StyledH4,
  StyledButton,
} from 'styles/app';
import colors from 'styles/colors';
import { useDispatch, useSelector } from 'react-redux';
import OverviewTabMenu from '../overview-tab-menu';
import AddChartPopup from '../add-chart-popup';
import TimeSeriesChart from '../composed-chart';

const StyledDataVisualization = styled.div`
  padding: 16px 20px;
  padding: 1rem 1.25rem;
  header {
    display: flex;
    h2 {
      margin-right: 4px;
      margin-right: 0.25rem;
      width: 108px;
    }
    ul {
      margin-top: 3px;
      margin-top: 0.1875rem;
    }
  }
  section {
    margin-top: 16px;
    margin-top: 1rem;
    background-color: ${colors.white};
    color: ${colors.gray10};
    border-radius: 6px;
    max-width: 972px;
    font-size: 18px;
    font-size: 1.125rem;
    line-height: 21px;
    line-height: 1.3125rem;
    padding: 18px 20px;
    padding: 1.125rem 1.5rem;
    h4 {
      margin-bottom: 40px;
      margin-bottom: 2.5rem;
    }
  }
`;

const AddChartButton = styled(StyledButton)`
  &.ant-btn {
    color: ${colors.grayText};
    height: 30px;
    font-weight: 300;
    &:hover {
      color: ${colors.lightBlue};
    }
    align-items: center;
    span:before {
      content: "+";
      font-size: 30px;
      font-size: 1.875rem;
      display: inline-block;
      margin-right: 4px;
      margin-right: 0.25rem;
    }
    span {
      display: flex;
    }
  }
`;

const DataVisualization = ({
  pipelineInView, pipelineRunSelected, sequence, setDisplayTab,
}) => {
  const [showAddChartPopup, setShowAddChartPopup] = useState(false);

  const currentOrg = useSelector((state) => state.user.currentOrg);
  const charts = useSelector((state) => state.charts.charts);
  const chartDatum = useSelector((state) => state.charts.chartDatum);
  const dispatch = useDispatch();

  const pipelineRunCharts = charts && charts[pipelineRunSelected && pipelineRunSelected.uuid];

  useEffect(() => {
    if (charts) return;

    dispatch(getCharts(currentOrg, pipelineInView, pipelineRunSelected && pipelineRunSelected.uuid));
  }, [currentOrg, pipelineInView, pipelineRunSelected, dispatch, charts]);

  useEffect(() => {
    if (!pipelineRunCharts) return;

    pipelineRunCharts.map(({ artifact }) => dispatch(processArtifact(artifact)));
  }, [pipelineRunCharts, dispatch]);

  return (
    <>
      <StyledDataVisualization>
        <header>
          <StyledH2 color="black">
            Run #
            {sequence}
          </StyledH2>
          <OverviewTabMenu
            displayTab={DATA_VISUALIZATION_TAB}
            setDisplayTab={setDisplayTab}
            dataVisualizationReady={pipelineRunSelected && pipelineRunSelected.status === pipelineStates.COMPLETED}
            consoleOutputReady={!!pipelineRunSelected}
          />
        </header>
        <AddChartButton
          color="white"
          width={130}
          onClick={() => setShowAddChartPopup(true)}
        >
          Add A Chart
        </AddChartButton>
        {pipelineRunCharts && pipelineRunCharts.map(({
          artifact, name: title, chart_type_code, chart_config,
        }) => (
          <section key={`${title}${artifact && artifact.uuid}${chart_type_code}`}>
            <StyledH4 color="black">{title}</StyledH4>
            {chart_type_code === CHART_TYPES.IMAGE_CHART && (
              <img src={artifact.url} alt={artifact.name} width="100%" />
            )}
            {chart_type_code === CHART_TYPES.LINE_CHART && artifact.url in chartDatum && (
              <TimeSeriesChart
                type={chart_type_code}
                config={chart_config}
                artifact={artifact}
                chartData={chartDatum[artifact.url].chartData}
                chartTypes={chartDatum[artifact.url].chartTypes}
                chartScales={chartDatum[artifact.url].chartScales}
              />
            )}
            {chart_type_code === CHART_TYPES.BAR_CHART && artifact.url in chartDatum && (
              <TimeSeriesChart
                type={chart_type_code}
                config={chart_config}
                artifact={artifact}
                chartData={chartDatum[artifact.url].chartData}
                chartTypes={chartDatum[artifact.url].chartTypes}
                chartScales={chartDatum[artifact.url].chartScales}
              />
            )}
          </section>
        ))}
      </StyledDataVisualization>
      {showAddChartPopup && (
        <AddChartPopup
          handleOk={() => setShowAddChartPopup(false)}
          handleCancel={() => setShowAddChartPopup(false)}
          pipeline_uuid={pipelineInView}
          pipeline_run_uuid={pipelineRunSelected && pipelineRunSelected.uuid}
          artifacts={pipelineRunSelected && pipelineRunSelected.artifacts}
        />
      )}
    </>
  );
};

DataVisualization.propTypes = {
  pipelineInView: PropTypes.string.isRequired,
  pipelineRunSelected: PropTypes.shape({
    uuid: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
    artifacts: PropTypes.arrayOf(PropTypes.shape({
      uuid: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      url: PropTypes.string.isRequired,
    })).isRequired,
  }).isRequired,
  sequence: PropTypes.number.isRequired,
  setDisplayTab: PropTypes.func.isRequired,
};

export default DataVisualization;
