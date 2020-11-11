import moment from 'moment';

export const chartTypes = {
  LINE_CHART: 'LINE_CHART',
  BAR_CHART: 'BAR_CHART',
  IMAGE_CHART: 'IMAGE_CHART',
};

export const XAXIS = 'x-axis';
export const YAXIS = 'y-axis';

export const AXES_LIMIT = 4;

// todo: to csv.
// strings.
export const mockData = [
  {
    timestamp: moment('2017-01-01 00:00:00').unix(),
    L1: 3352,
    L2: 1298,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-01 12:00:00').unix(),
    L1: 3652,
    L2: 8298,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-02 00:00:00').unix(),
    L1: 5652,
    L2: 9098,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-02 12:00:00').unix(),
    L1: 12352,
    L2: 1898,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-03 00:00:00').unix(),
    L1: 3352,
    L2: 298,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-03 12:00:00').unix(),
    L1: 3652,
    L2: 998,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-04 00:00:00').unix(),
    L1: 552,
    L2: 3298,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-04 12:00:00').unix(),
    L1: 12352,
    L2: 10098,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-05 00:00:00').unix(),
    L1: 3352,
    L2: 4998,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-05 12:00:00').unix(),
    L1: 8652,
    L2: 1008,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-06 00:00:00').unix(),
    L1: 7652,
    L2: 4898,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-06 12:00:00').unix(),
    L1: 13352,
    L2: 8298,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-07 00:00:00').unix(),
    L1: 10352,
    L2: 14398,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
  {
    timestamp: moment('2017-01-07 12:00:00').unix(),
    L1: 552,
    L2: 3988,
    L3: Math.round(Math.random() * 20000 + 500),
    L4: Math.round(Math.random() * 20000 + 500),
  },
];
