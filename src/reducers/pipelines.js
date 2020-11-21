import { computePipelineRunMetaData, createdAtSort } from 'util/data';
import {
  GET_PIPELINES,
  GET_PIPELINES_FAILED,
  GET_PIPELINE_RUNS,
  GET_PIPELINE_RUNS_FAILED,
  GET_PIPELINE_RUN,
  GET_PIPELINE_RUN_IN_PROGRESS,
  GET_PIPELINE_RUN_FAILED,
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
    getPipelineRunInProgress: false,
    getPipelineRunError: null,
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
        currentPipelineRun: pipelineRuns.length && pipelineRuns[0],
        currentPipelineRunUuid: pipelineRuns.length && pipelineRuns[0].uuid,
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
      const { pipelineRun, pipeline_uuid, pipeline_run_uuid } = action.payload;

      if (!(pipeline_uuid in state.pipelineRuns)) return state;

      const pipelineRuns = [...state.pipelineRuns[pipeline_uuid]] || [];
      const currentPipelineRun = computePipelineRunMetaData(pipelineRun);
      const pipelineRunIndex = pipelineRuns.findIndex((run) => run.uuid === pipeline_run_uuid);

      if (pipelineRunIndex === -1) return state;

      pipelineRuns[pipelineRunIndex] = currentPipelineRun;

      return {
        ...state,
        pipelineRuns: {
          ...state.pipelineRuns,
          [pipeline_uuid]: pipelineRuns,
        },
        currentPipelineRun,
        currentPipelineRunUuid: pipeline_run_uuid,
        messages: DEFAULT_STATE.messages,
      };
    }
    case GET_PIPELINE_RUN_IN_PROGRESS:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          getPipelineRunInProgress: true,
        },
      };
    case GET_PIPELINE_RUN_FAILED:
      return {
        ...state,
        currentPipelineRun: null,
        currentPipelineRunUuid: null,
        messages: {
          ...DEFAULT_STATE.messages,
          getPipelineRunError: action.payload,
        },
      };
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
