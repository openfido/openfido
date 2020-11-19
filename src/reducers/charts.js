import {
  ADD_CHART,
  ADD_CHART_FAILED,
  GET_CHARTS,
  GET_CHARTS_FAILED,
  PROCESS_ARTIFACT,
  PROCESS_ARTIFACT_FAILED,
} from 'actions';

const DEFAULT_STATE = {
  charts: null,
  messages: {
    getChartsError: null,
    addChartError: null,
    processArtifactError: null,
  },
  chartDatum: {},
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case PROCESS_ARTIFACT:
      return {
        ...state,
        chartDatum: {
          ...state.chartDatum,
          [action.artifact.url]: {
            chartData: action.chartData,
            chartTypes: action.chartTypes,
            chartScales: action.chartScales,
          },
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
        charts: {
          ...state.charts,
          [pipeline_run_uuid]: charts,
        },
      };
    }
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
    default:
      return state;
  }
};
