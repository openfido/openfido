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

export const mockData = `datetime,type,subtype,L1,L2,L3,L4
"2017-01-01 00:00:00","energy","high",32,203,398,20000
"2017-01-01 06:00:00","energy","high",32,203,398,20000
"2017-01-01 12:00:00","energy","low",422,778,891,20000
"2017-01-02 00:00:00","energy","medium",12432,203,387,20000
"2017-01-02 06:00:00","energy","medium",12432,203,387,20000
"2017-01-02 12:00:00","bad energy","high",2152,3778,5891,20000
"2017-01-03 00:00:00","energy","medium",9432,203,387,20000
"2017-01-03 06:00:00","energy","medium",9432,203,387,20000
"2017-01-03 12:00:00","energy","medium",552,978,8891,20000
"2017-01-04 00:00:00","energy","high",132,2033,4387,20000
"2017-01-04 06:00:00","energy","high",132,2033,4387,20000
"2017-01-04 12:00:00","energy","low",21352,34778,7891,20000
"2017-01-05 00:00:00","energy","high",32,203,398,20000
"2017-01-05 06:00:00","energy","high",32,203,398,20000
"2017-01-05 12:00:00","energy","low",422,778,891,20000
"2017-01-06 00:00:00","energy","medium",12432,203,387,20000
"2017-01-06 06:00:00","energy","medium",12432,203,387,20000
"2017-01-06 12:00:00","energy","high",2152,3778,5891,20000
"2017-01-07 00:00:00","energy","medium",9432,203,387,20000
"2017-01-07 06:00:00","energy","medium",9432,203,387,20000
"2017-01-07 12:00:00","energy","medium",552,978,8891,20000
"2017-01-08 00:00:00","energy","high",132,2033,4387,20000
"2017-01-08 06:00:00","energy","high",132,2033,4387,20000
"2017-01-08 12:00:00","energy","low",21352,34778,7891,20000
"2017-01-09 00:00:00","energy","high",32,203,398,20000
"2017-01-09 06:00:00","energy","high",32,203,398,20000
"2017-01-09 12:00:00","energy","low",422,778,891,20000
"2017-01-10 00:00:00","energy","medium",12432,203,387,20000
"2017-01-10 06:00:00","energy","medium",12432,203,387,20000
"2017-01-10 12:00:00","energy","high",2152,3778,5891,20000
"2017-01-11 00:00:00","energy","medium",9432,203,387,20000
"2017-01-11 06:00:00","energy","medium",9432,203,387,20000
"2017-01-11 12:00:00","energy","medium",552,978,8891,20000
"2017-01-12 00:00:00","energy","high",132,2033,4387,20000
"2017-01-12 06:00:00","energy","high",132,2033,4387,20000
"2017-01-12 12:00:00","energy","low",21352,34778,7891,20000`;
