import colors from 'styles/colors';

export const CHART_TYPES = {
  LINE_CHART: 'LINE_CHART',
  BAR_CHART: 'BAR_CHART',
  IMAGE_CHART: 'IMAGE_CHART',
};

export const DATA_TYPES = {
  NUMBER: 'number',
  TIME: 'time',
  CATEGORY: 'category',
};

export const DATA_SCALES = {
  TIME: 'time',
  LINEAR: 'linear',
  AUTO: 'auto',
};

export const XAXIS = 'x-axis';
export const YAXIS = 'y-axis';

export const AXES_LIMIT = 4;

export const chartFills = [
  colors.chartBlue,
  colors.chartGray,
  colors.chartGreen,
  colors.chartYellow,
];

export const chartStrokes = [
  colors.chartBlue,
  colors.chartGrayStroke,
  colors.chartGreen,
  colors.chartYellow,
];

export const CHART_TITLE_LENGTH_LIMIT = 128;
