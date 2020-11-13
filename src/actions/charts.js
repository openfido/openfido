import {
  GET_CHARTS,
  GET_CHARTS_FAILED,
  ADD_CHART,
  ADD_CHART_FAILED,
} from 'actions';
import {
  requestOrganizationPipelineRunCharts,
  requestCreatePipelineRunArtifact,
} from 'services';

export const getCharts = (organization_uuid, pipeline_uuid, pipeline_run_uuid) => (dispatch) => (
  requestOrganizationPipelineRunCharts(organization_uuid, pipeline_uuid, pipeline_run_uuid)
    .then((response) => {
      dispatch({
        type: GET_CHARTS,
        payload: {
          pipeline_run_uuid,
          charts: response.data,
        },
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_CHARTS_FAILED,
        payload: !err.response || err.response.data,
      });
    })
);

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
