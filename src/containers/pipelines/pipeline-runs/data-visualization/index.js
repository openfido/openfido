import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';

import { getCharts } from 'actions/charts';
import { CHART_TYPES } from 'config/charts';
import {
  StyledH2,
  StyledH4,
  StyledButton,
  StyledTitle,
  StyledText,
} from 'styles/app';
import colors from 'styles/colors';
import { getPipelines, getPipelineRun } from 'actions/pipelines';
import OverviewTabMenu from '../overview-tab-menu';
import AddChartPopup from '../add-chart-popup';
import ComposedCsvChart from '../composed-csv-chart';

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
    min-height: 351px;
    h4 {
      margin-bottom: 8px;
      margin-bottom: 0.5rem;
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

const DataVisualization = () => {
  const { pipeline_uuid: pipelineInView, pipeline_run_uuid: pipelineRunSelectedUuid } = useParams();

  const [showAddChartPopup, setShowAddChartPopup] = useState(false);

  const currentOrg = useSelector((state) => state.user.currentOrg);
  const charts = useSelector((state) => state.charts.charts);
  const chartDatum = useSelector((state) => state.charts.chartDatum);
  const pipelines = useSelector((state) => state.pipelines.pipelines);
  const currentPipelineRun = useSelector((state) => state.pipelines.currentPipelineRun);
  const currentPipelineRunUuid = useSelector((state) => state.pipelines.currentPipelineRunUuid);
  const dispatch = useDispatch();

  const pipelineRunCharts = charts && charts[pipelineRunSelectedUuid];
  const pipelineItemInView = pipelines && pipelines.find((pipelineItem) => pipelineItem.uuid === pipelineInView);
  const pipelineRunArtifacts = currentPipelineRun && currentPipelineRun.artifacts;

  useEffect(() => {
    if (!pipelines && !pipelineItemInView) {
      dispatch(getPipelines(currentOrg));
    }
  }, [currentOrg, dispatch, pipelines, pipelineItemInView]);

  useEffect(() => {
    if (currentPipelineRunUuid !== pipelineRunSelectedUuid) {
      dispatch(getPipelineRun(currentOrg, pipelineInView, pipelineRunSelectedUuid));
    }
  }, [currentOrg, pipelineInView, pipelineRunSelectedUuid, currentPipelineRunUuid, dispatch]);

  useEffect(() => {
    if (charts && pipelineRunSelectedUuid in charts) return;

    dispatch(getCharts(currentOrg, pipelineInView, pipelineRunSelectedUuid));
  }, [currentOrg, pipelineInView, pipelineRunSelectedUuid, dispatch, charts]);

  return (
    <>
      <StyledTitle>
        <div>
          <h1>
            Pipeline Runs:
            {' '}
            <StyledText color="blue">{pipelineItemInView && pipelineItemInView.name}</StyledText>
          </h1>
        </div>
      </StyledTitle>
      <StyledDataVisualization>
        <header>
          <StyledH2 color="black">
            Run #
            {currentPipelineRun && currentPipelineRun.sequence}
          </StyledH2>
          <OverviewTabMenu
            dataVisualizationReady
            consoleOutputReady
            pipelineInView={pipelineInView}
            pipelineRunSelectedUuid={pipelineRunSelectedUuid}
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
          <section key={`${title}${artifact && artifact.uuid}${chart_type_code}${Math.random()}`}>
            <StyledH4 color="black">{title}</StyledH4>
            {chart_type_code === CHART_TYPES.IMAGE_CHART && (
              <img src={artifact.url} alt={artifact.name} width="100%" />
            )}
            {chart_type_code === CHART_TYPES.LINE_CHART && artifact.url in chartDatum && (
              <ComposedCsvChart
                type={chart_type_code}
                config={chart_config}
                artifact={artifact}
                chartData={chartDatum[artifact.url].chartData}
                chartTypes={chartDatum[artifact.url].chartTypes}
                chartScales={chartDatum[artifact.url].chartScales}
              />
            )}
            {chart_type_code === CHART_TYPES.BAR_CHART && artifact.url in chartDatum && (
              <ComposedCsvChart
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
          pipeline_run_uuid={pipelineRunSelectedUuid}
          artifacts={pipelineRunArtifacts}
        />
      )}
    </>
  );
};

export default DataVisualization;
