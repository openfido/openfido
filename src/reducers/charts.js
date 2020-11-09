import {
  ADD_CHART,
  ADD_CHART_FAILED,
} from 'actions';

const DEFAULT_STATE = {
  charts: {},
  messages: {
    addChartError: null,
  },
};

export default (state = DEFAULT_STATE, action) => {
  if (action.error) return state;

  switch (action.type) {
    case ADD_CHART: {
      const { pipeline_run_uuid, chart } = action.payload; // TODO: formatted graph data

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
