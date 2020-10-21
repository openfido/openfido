import {
  GET_PIPELINES,
  GET_PIPELINES_FAILED,
  ADD_PIPELINE,
  DELETE_PIPELINE,
} from 'actions';
import { requestGetPipelines } from 'services';

export const getPipelines = (organization_uuid) => (dispatch) => {
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

export const addPipeline = (payload) => ({
  type: ADD_PIPELINE,
  payload,
});

export const deletePipeline = (payload) => ({
  type: DELETE_PIPELINE,
  payload,
});
