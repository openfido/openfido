import {
  GET_PIPELINES,
  GET_PIPELINES_FAILED,
  UPLOAD_INPUT_FILE,
  UPLOAD_INPUT_FILE_FAILED,
  REMOVE_INPUT_FILE,
  CLEAR_INPUT_FILES,
} from 'actions';

const DEFAULT_STATE = {
  pipelines: null,
  inputFiles: null,
  messages: {
    getPipelinesError: null,
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
