import colors from 'styles/colors';

export const chartTypes = {
  LINE_CHART: 'LINE_CHART',
  BAR_CHART: 'BAR_CHART',
  IMAGE_CHART: 'IMAGE_CHART',
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

export const mockData = `datetime,type,subtype,L1,L2,L3
"2017-01-01 00:00:00","energy","high",32,203,398
"2017-01-01 12:00:00","energy","low",422,778,891
"2017-01-02 00:00:00","energy","medium",12432,203,387
"2017-01-02 12:00:00","energy","high",2152,3778,5891
"2017-01-03 00:00:00","energy","medium",9432,203,387
"2017-01-03 12:00:00","energy","medium",552,978,8891
"2017-01-04 00:00:00","energy","high",132,2033,4387
"2017-01-04 12:00:00","energy","low",21352,34778,7891`;
