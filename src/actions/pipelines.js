import {
  GET_PIPELINES,
  GET_PIPELINES_FAILED,
  ADD_PIPELINE,
  DELETE_PIPELINE,
  UPLOAD_INPUT_FILE,
  UPLOAD_INPUT_FILE_FAILED,
  REMOVE_INPUT_FILE,
  CLEAR_INPUT_FILES,
} from 'actions';
import { requestGetPipelines, requestUploadInputFile } from 'services';

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
