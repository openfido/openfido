import {
  GET_PIPELINES,
  GET_PIPELINES_IN_PROGRESS,
  GET_PIPELINES_FAILED,
  GET_PIPELINE_RUNS,
  GET_PIPELINE_RUNS_IN_PROGRESS,
  GET_PIPELINE_RUNS_FAILED,
  GET_PIPELINE_RUN,
  GET_PIPELINE_RUN_IN_PROGRESS,
  GET_PIPELINE_RUN_FAILED,
  GET_PIPELINE_RUN_CONSOLE_OUTPUT,
  GET_PIPELINE_RUN_CONSOLE_OUTPUT_IN_PROGRESS,
  GET_PIPELINE_RUN_CONSOLE_OUTPUT_FAILED,
  UPLOAD_INPUT_FILE,
  UPLOAD_INPUT_FILE_FAILED,
  REMOVE_INPUT_FILE,
  CLEAR_INPUT_FILES,
} from 'actions';
import {
  requestGetPipelines,
  requestGetPipelineRuns,
  requestGetPipelineRun,
  requestPipelineRunConsoleOutput,
  requestUploadInputFile,
} from 'services';

export const getPipelines = (organization_uuid) => async (dispatch) => {
  await dispatch({ type: GET_PIPELINES_IN_PROGRESS });
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
    });
};

export const getPipelineRuns = (organization_uuid, pipeline_uuid) => async (dispatch) => {
  await dispatch({ type: GET_PIPELINE_RUNS_IN_PROGRESS });
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
    });
};

export const getPipelineRun = (organization_uuid, pipeline_uuid, pipeline_run_uuid) => async (dispatch) => {
  await dispatch({ type: GET_PIPELINE_RUN_IN_PROGRESS });
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
    });
};

// Adds current pipeline run's console output to the console field in state
export const getPipelineRunConsoleOutput = (organization_uuid, pipeline_uuid, pipeilne_run_uuid, poll) => async (dispatch) => {
  if (!poll) await dispatch({ type: GET_PIPELINE_RUN_CONSOLE_OUTPUT_IN_PROGRESS });
  requestPipelineRunConsoleOutput(organization_uuid, pipeline_uuid, pipeilne_run_uuid)
    .then((response) => {
      dispatch({
        type: GET_PIPELINE_RUN_CONSOLE_OUTPUT,
        payload: response.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_PIPELINE_RUN_CONSOLE_OUTPUT_FAILED,
        payload: !err.response || err.response.data,
      });
    });
};

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
