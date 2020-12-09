import {
  ADD_CHART,
  ADD_CHART_FAILED,
  GET_CHARTS,
  GET_CHARTS_IN_PROGRESS,
  GET_CHARTS_FAILED,
  PROCESS_ARTIFACT,
  PROCESS_ARTIFACT_IN_PROGRESS,
  PROCESS_ARTIFACT_FAILED,
  SET_GRAPH_MIN_MAX,
  UPDATE_CHART,
  DELETE_CHART,
} from 'actions';

const DEFAULT_STATE = {
  charts: null,
  messages: {
    getChartsError: null,
    getChartsInProgress: false,
    addChartError: null,
    processArtifactInProgress: false,
    processArtifactError: null,
  },
  chartDatum: {},
  graphMinMax: {},
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case PROCESS_ARTIFACT:
      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        chartDatum: {
          ...state.chartDatum,
          [action.artifact.url]: {
            chartData: action.chartData,
            chartTypes: action.chartTypes,
            chartScales: action.chartScales,
          },
        },
        graphMinMax: {
          ...state.graphMinMax,
          [action.pipeline_run_uuid]: {
            ...state.graphMinMax[action.pipeline_run_uuid],
            [action.chartIndex]: {
              min: action.minIndex,
              max: action.maxIndex,
            },
          },
        },
      };
    case PROCESS_ARTIFACT_IN_PROGRESS:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          processArtifactInProgress: true,
        },
      };
    case PROCESS_ARTIFACT_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          processArtifactError: action.payload,
        },
      };
    case GET_CHARTS: {
      const { pipeline_run_uuid, charts } = action.payload;

      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        charts: {
          ...state.charts,
          [pipeline_run_uuid]: charts,
        },
      };
    }
    case GET_CHARTS_IN_PROGRESS:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          getChartsInProgress: true,
        },
      };
    case GET_CHARTS_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          getChartsError: action.payload,
        },
      };
    case ADD_CHART: {
      const { pipeline_run_uuid, chart } = action.payload;

      const pipelineRunCharts = (pipeline_run_uuid in state.charts && [...state.charts[pipeline_run_uuid]]) || [];
      pipelineRunCharts.push(chart);

      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        charts: {
          ...state.charts,
          [pipeline_run_uuid]: pipelineRunCharts,
        },
      };
    }
    case ADD_CHART_FAILED:
      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          addChartError: action.payload,
        },
      };
    case SET_GRAPH_MIN_MAX: {
      const {
        pipeline_run_uuid, index, min, max,
      } = action.payload;

      const pipelineRunGraphMinMax = state.graphMinMax[pipeline_run_uuid] || {};

      pipelineRunGraphMinMax[index] = { min, max };

      return {
        ...state,
        messages: DEFAULT_STATE.messages,
        graphMinMax: {
          ...state.graphMinMax,
          [pipeline_run_uuid]: pipelineRunGraphMinMax,
        },
      };
    }
    case UPDATE_CHART: {
      const pipelineRunCharts = state.charts[action.payload.pipelineRunUuid];

      pipelineRunCharts.forEach((chart) => {
        if (chart.uuid === action.payload.chartUuid) {
          chart.name = action.payload.name;
        }
      });

      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
        },
        charts: {
          ...state.charts,
          [action.payload.pipelineRunUuid]: pipelineRunCharts,
        }
      }
    }
    case DELETE_CHART: {
      const pipelineRunCharts = state.charts[action.payload.pipelineRunUuid];

      return {
        ...state,
        messages: {
          ...DEFAULT_STATE.messages,
          deleteChartError: action.payload,
        },
        charts: {
          ...state.charts,
          [action.payload.pipelineRunUuid]: pipelineRunCharts.filter((chart) => action.payload.chartUuid !== chart.uuid),
        },
      }
    }
    default:
      return state;
  }
};
