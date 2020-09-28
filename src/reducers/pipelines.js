import {
  GET_PIPELINES_STARTED,
  GET_PIPELINES_COMPLETED,
  GET_PIPELINES_FAILED,
  ADD_PIPELINE,
  DELETE_PIPELINE,
} from 'actions';
import { USER_KEY_PIPELINES } from 'util/storage';

const DEFAULT_STATE = {
  pipelines: [],
  pipelineNewImport: {},
  isLoadingPipelines: false,
  error: null,
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case GET_PIPELINES_STARTED:
      return {
        ...state,
        isLoadingPipelines: true,
        error: null,
      };
    case GET_PIPELINES_COMPLETED: {
      let localPipelines = window.localStorage.getItem(USER_KEY_PIPELINES);

      try {
        localPipelines = localPipelines.length ? JSON.parse(localPipelines) : [];
      } catch (e) {
        localPipelines = action.payload;
      }

      window.localStorage.setItem(USER_KEY_PIPELINES, JSON.stringify(localPipelines));

      return {
        ...state,
        pipelines: localPipelines,
        isLoadingPipelines: false,
        error: null,
      };
    }
    case GET_PIPELINES_FAILED:
      return {
        ...state,
        isLoadingPipelines: false,
        error: action.payload,
      };
    case ADD_PIPELINE: {
      const localPipelines = [
        ...state.pipelines,
        {
          id: Math.random(), // TODO: auto-increment that works with delete would be nice
          name: action.payload.name,
          last_updated: 'a few seconds ago',
        },
      ];
      window.localStorage.setItem(USER_KEY_PIPELINES, JSON.stringify(localPipelines));

      return {
        ...state,
        pipelines: localPipelines,
      };
    }
    case DELETE_PIPELINE: {
      const localPipelines = state.pipelines.filter((item) => item.id !== action.payload.id);
      window.localStorage.setItem(USER_KEY_PIPELINES, JSON.stringify(localPipelines));

      return {
        ...state,
        pipelines: localPipelines,
      };
    }
    default:
      return state;
  }
};
