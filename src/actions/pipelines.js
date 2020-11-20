import {
  GET_PIPELINES,
  GET_PIPELINES_FAILED,
  ADD_PIPELINE,
  DELETE_PIPELINE,
  GET_PIPELINE_RUNS,
  GET_PIPELINE_RUNS_FAILED,
  GET_PIPELINE_RUN,
  GET_PIPELINE_RUN_FAILED,
  UPLOAD_INPUT_FILE,
  UPLOAD_INPUT_FILE_FAILED,
  REMOVE_INPUT_FILE,
  CLEAR_INPUT_FILES,
} from 'actions';
import {
  requestGetPipelines,
  requestGetPipelineRuns,
  requestGetPipelineRun,
  requestUploadInputFile,
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
        payload: {
          pipelineRuns: response.data,
          pipeline_uuid,
        },
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_PIPELINE_RUNS_FAILED,
        payload: !err.response || err.response.data,
      });
    })
);

export const getPipelineRun = (organization_uuid, pipeline_uuid, pipeline_run_uuid) => (dispatch) => (
  requestGetPipelineRun(organization_uuid, pipeline_uuid, pipeline_run_uuid)
    .then((response) => {
      dispatch({
        type: GET_PIPELINE_RUN,
        payload: {
          pipelineRun: response.data,
          pipeline_uuid,
          pipeline_run_uuid,
        },
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_PIPELINE_RUN_FAILED,
        payload: !err.response || err.response.data,
      });
    })
);

export const uploadInputFile = (organization_uuid, pipeline_uuid, file_name, file_content) => (dispatch) => (
  requestUploadInputFile(organization_uuid, pipeline_uuid, file_name, file_content)
    .then((response) => {
      dispatch({
        type: UPLOAD_INPUT_FILE,
        payload: response.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: UPLOAD_INPUT_FILE_FAILED,
        payload: !err.response || err.response.data,
      });
    })
);

export const removeInputFile = (payload) => ({
  type: REMOVE_INPUT_FILE,
  payload,
});

export const clearInputFiles = (payload) => ({
  type: CLEAR_INPUT_FILES,
  payload,
});
