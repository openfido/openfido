import { computePipelineRunMetaData, createdAtSort } from 'util/data';
import {
  GET_PIPELINES,
  GET_PIPELINES_FAILED,
  GET_PIPELINE_RUNS,
  GET_PIPELINE_RUNS_FAILED,
  GET_PIPELINE_RUN,
  GET_PIPELINE_RUN_FAILED,
  SELECT_PIPELINE_RUN,
  UPLOAD_INPUT_FILE,
  UPLOAD_INPUT_FILE_FAILED,
  REMOVE_INPUT_FILE,
  CLEAR_INPUT_FILES,
} from 'actions';

const DEFAULT_STATE = {
  pipelines: null,
  pipelineRuns: {},
  inputFiles: null,
  currentPipelineRun: null,
  currentPipelineRunUuid: null,
  messages: {
    getPipelinesError: null,
    getPipelineRunsError: null,
    uploadInputFileError: null,
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

      pipelines.forEach((pipeline) => {
        const { last_pipeline_run = {} } = pipeline;
        const { states = [] } = last_pipeline_run;

        states.sort(createdAtSort);
      });

      return {
        ...state,
        messages: DEFAULT_STATE.messages,
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
    case GET_PIPELINE_RUNS: {
      const { pipelineRuns = [], pipeline_uuid } = action.payload;

      pipelineRuns.sort((runA, runB) => {
        if (runA.sequence && runB.sequence) {
          return runB.sequence - runA.sequence;
        }

        return -1;
      });

      pipelineRuns.forEach((run, index) => {
        pipelineRuns[index] = computePipelineRunMetaData(run);
      });

      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        pipelineRuns: {
          ...state.pipelineRuns,
          [pipeline_uuid]: pipelineRuns,
        },
      };
    }
    case GET_PIPELINE_RUNS_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          getPipelineRunsError: action.payload,
        },
      };
    case GET_PIPELINE_RUN: {
      const { pipelineRun, pipeline_run_uuid } = action.payload;

      computePipelineRunMetaData(pipelineRun);

      return {
        ...state,
        currentPipelineRun: pipelineRun,
        currentPipelineRunUuid: pipeline_run_uuid,
        messages: DEFAULT_STATE.messages,
      };
    }
    case SELECT_PIPELINE_RUN:
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        currentPipelineRunUuid: action.payload,
      };
    case GET_PIPELINE_RUN_FAILED: {
      return {
        ...state,
        currentPipelineRun: null,
        currentPipelineRunUuid: null,
        messages: DEFAULT_STATE.messages,
      };
    }
    case UPLOAD_INPUT_FILE:
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        inputFiles: state.inputFiles ? (
          [
            ...state.inputFiles,
            action.payload,
          ]
        ) : (
          [
            action.payload,
          ]
        ),
      };
    case UPLOAD_INPUT_FILE_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          uploadInputFileError: action.payload,
        },
      };
    case REMOVE_INPUT_FILE: {
      const inputFiles = [...state.inputFiles];
      inputFiles.splice(action.payload, 1);

      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        inputFiles,
      };
    }
    case CLEAR_INPUT_FILES:
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        inputFiles: null,
      };
    default:
      return state;
  }
};
