import {
  GET_CHARTS,
  GET_CHARTS_IN_PROGRESS,
  GET_CHARTS_FAILED,
  ADD_CHART,
  ADD_CHART_FAILED,
  PROCESS_ARTIFACT,
  PROCESS_ARTIFACT_IN_PROGRESS,
  PROCESS_ARTIFACT_FAILED,
  SET_GRAPH_MIN_MAX,
  UPDATE_CHART,
  DELETE_CHART,
} from 'actions';
import {
  requestPipelineRunCharts,
  requestCreatePipelineRunArtifact,
  requestArtifact,
} from 'services';
import { parseCsvData } from 'util/charts';

export const processArtifact = (artifact) => (dispatch, getState) => {
  const { chartDatum } = getState().charts;
  if (artifact.url in chartDatum) return;

  requestArtifact(artifact)
    .then((response) => response.text())
    .then((data) => parseCsvData(data))
    .then(({ chartData, chartTypes, chartScales }) => {
      dispatch({
        type: PROCESS_ARTIFACT,
        artifact,
        chartData,
        chartTypes,
        chartScales,
      });
    })
    .catch((err) => {
      dispatch({
        type: PROCESS_ARTIFACT_FAILED,
        payload: err.message || (!err.response || err.response.data),
      });
    });
};

export const getCharts = (organization_uuid, pipeline_uuid, pipeline_run_uuid) => async (dispatch) => {
  await dispatch({ type: GET_CHARTS_IN_PROGRESS });
  requestPipelineRunCharts(organization_uuid, pipeline_uuid, pipeline_run_uuid)
    .then((chartsResponse) => {
      const { data: charts } = chartsResponse;

      dispatch({
        type: GET_CHARTS,
        payload: {
          pipeline_run_uuid,
          charts,
        },
      });

      if (!charts || !charts.length) return;

      charts.forEach(async (chart, chartIndex) => {
        const { artifact } = chart;

        if (!artifact) return;

        await dispatch({ type: PROCESS_ARTIFACT_IN_PROGRESS });
        requestArtifact(artifact)
          .then((artifactResponse) => artifactResponse.text())
          .then((data) => parseCsvData(data))
          .then(({ chartData, chartTypes, chartScales }) => {
            dispatch({
              type: PROCESS_ARTIFACT,
              artifact,
              chartData,
              chartTypes,
              chartScales,
              chartIndex,
              minIndex: 0,
              maxIndex: chartData.length - 1,
              pipeline_run_uuid,
            });
          })
          .catch((err) => {
            dispatch({
              type: PROCESS_ARTIFACT_FAILED,
              payload: err.message || (!err.response || err.response.data),
            });
          });
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_CHARTS_FAILED,
        payload: !err.response || err.response.data,
      });
    });
};

export const addChart = (organization_uuid, pipeline_uuid, pipeline_run_uuid, title, artifact_uuid, chart_type_code, chart_config) => (dispatch) => (
  requestCreatePipelineRunArtifact(organization_uuid, pipeline_uuid, pipeline_run_uuid, title, artifact_uuid, chart_type_code, chart_config)
    .then((response) => {
      dispatch({
        type: ADD_CHART,
        payload: {
          pipeline_run_uuid,
          chart: response.data,
        },
      });
    })
    .catch((err) => {
      dispatch({
        type: ADD_CHART_FAILED,
        payload: !err.response || err.response.data,
      });
    })
);

export const setGraphMinMax = (pipeline_run_uuid, index, min, max) => ({
  type: SET_GRAPH_MIN_MAX,
  payload: {
    pipeline_run_uuid,
    index,
    min,
    max,
  },
});

export const updateChart = (orgUuid, pipelineUuid, pipelineRunUuid, chartUuid, name) => ({
  type: UPDATE_CHART,
  payload: {
    orgUuid,
    pipelineUuid,
    pipelineRunUuid,
    chartUuid,
    name,
  },
});

export const deleteChart = (pipelineRunUuid, chartUuid) => ({
  type: DELETE_CHART,
  payload: {
    pipelineRunUuid,
    chartUuid,
  },
});
