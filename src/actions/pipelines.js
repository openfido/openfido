import {
  GET_PIPELINES_STARTED,
  GET_PIPELINES_COMPLETED,
  GET_PIPELINES_FAILED,
  ADD_PIPELINE,
  DELETE_PIPELINE,
} from 'actions';
import ApiClient from 'util/api-client';

export const getPipelinesStarted = () => ({
  type: GET_PIPELINES_STARTED,
});

export const getPipelinesCompleted = (payload) => ({
  type: GET_PIPELINES_COMPLETED,
  payload,
});

export const getPipelinesFailed = (error) => ({
  type: GET_PIPELINES_FAILED,
  payload: error,
});

export const getPipelines = () => (dispatch) => {
  dispatch(getPipelinesStarted());
  ApiClient.get('/v1/pipelines')
    .then((res) => {
      dispatch(getPipelinesCompleted(res.data));
    })
    .catch((err) => {
      dispatch(getPipelinesFailed(err));
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
