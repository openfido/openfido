import moment from 'moment';

import { pipelineStates } from 'config/pipeline-status';
import {
  GET_PIPELINES,
  GET_PIPELINES_FAILED,
  GET_PIPELINE_RUNS,
  GET_PIPELINE_RUNS_FAILED,
  UPLOAD_INPUT_FILE,
  UPLOAD_INPUT_FILE_FAILED,
  REMOVE_INPUT_FILE,
  CLEAR_INPUT_FILES,
} from 'actions';

const DEFAULT_STATE = {
  pipelines: null,
  pipelineRuns: {},
  inputFiles: null,
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
    case GET_PIPELINE_RUNS: {
      const { pipelineRuns = [], pipeline_uuid } = action.payload;

      pipelineRuns.sort((runA, runB) => {
        if (runA.sequence && runB.sequence) {
          return runB.sequence - runA.sequence;
        }

        return -1;
      });

      pipelineRuns.forEach((run, index) => {
        const { states } = run;

        if (states) {
          states.sort((stateA, stateB) => {
            const dateA = moment(stateA.created_at);
            const dateB = moment(stateB.created_at);

            if (dateA && dateB) {
              return dateA - dateB;
            }

            return -1;
          });
        }

        let status = null;
        let startedAt = null;
        let completedAt = null;
        let momentStartedAt = null;
        let momentCompletedAt = null;
        let duration = null;

        if (states && states.length) {
          status = states[states.length - 1].state;
          startedAt = states.find((stateItem) => stateItem.state === pipelineStates.RUNNING);
          completedAt = states.find((stateItem) => (
            stateItem.state === pipelineStates.COMPLETED
              || stateItem.state === pipelineStates.FAILED
              || stateItem.state === pipelineStates.CANCELED
          ));

          startedAt = startedAt && startedAt.created_at;
          completedAt = completedAt && completedAt.created_at;

          momentStartedAt = startedAt && moment.utc(startedAt).local();
          momentCompletedAt = completedAt && moment.utc(completedAt).local();

          if (momentStartedAt && momentCompletedAt) {
            duration = moment.duration(momentStartedAt.diff(momentCompletedAt)).humanize();
          }
        }

        pipelineRuns[index].status = status;
        pipelineRuns[index].startedAt = momentStartedAt;
        pipelineRuns[index].completedAt = momentCompletedAt;
        pipelineRuns[index].duration = duration;
      });

      return {
        ...state,
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
