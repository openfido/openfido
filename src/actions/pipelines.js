import {
  GET_PIPELINES,
  GET_PIPELINES_FAILED,
  ADD_PIPELINE,
  DELETE_PIPELINE,
  GET_PIPELINE_RUNS,
  GET_PIPELINE_RUNS_FAILED,
} from 'actions';
import {
  requestGetPipelines,
  requestGetPipelineRuns,
} from 'services';

export const getPipelines = (organization_uuid) => (dispatch) => (
  requestGetPipelines(organization_uuid)
    .then((response) => {
      dispatch({
        type: GET_PIPELINES,
        payload: response.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_PIPELINES_FAILED,
        payload: !err.response || err.response.data,
      });
    })
);

export const addPipeline = (payload) => ({
  type: ADD_PIPELINE,
  payload,
});

export const deletePipeline = (payload) => ({
  type: DELETE_PIPELINE,
  payload,
});

export const getPipelineRuns = (organization_uuid, pipeline_uuid) => (dispatch) => (
  requestGetPipelineRuns(organization_uuid, pipeline_uuid)
    .then((response) => {
      dispatch({
        type: GET_PIPELINE_RUNS,
        payload: response.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_PIPELINE_RUNS_FAILED,
        payload: !err.response || err.response.data,
      });
    })
);
