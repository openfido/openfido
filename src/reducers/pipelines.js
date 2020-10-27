import {
  GET_PIPELINES,
  GET_PIPELINES_FAILED,
  GET_PIPELINE_RUNS,
  GET_PIPELINE_RUNS_FAILED,
} from 'actions';

const DEFAULT_STATE = {
  pipelines: null,
  pipelineRuns: null,
  messages: {
    getPipelinesError: null,
    getPipelineRunsError: null,
  },
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case GET_PIPELINES: {
      const pipelines = action.payload || [];

      pipelines.sort((pipelineA, pipelineB) => {
        if (pipelineA.name && pipelineB.name) {
          return pipelineA.name.localeCompare(pipelineB.name);
        }

        return -1;
      });

      return {
        ...state,
        pipelines: action.payload,
      };
    }
    case GET_PIPELINES_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          getPipelinesError: action.payload,
        },
      };
    case GET_PIPELINE_RUNS:
      return {
        ...state,
        pipelineRuns: action.payload,
      };
    case GET_PIPELINE_RUNS_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          getPipelineRunsError: action.payload,
        },
      };
    default:
      return state;
  }
};
