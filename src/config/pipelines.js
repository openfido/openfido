export const STDOUT = 'std_out';
export const STDERR = 'std_err';

export const POLL_PIPELINE_RUN_INTERVAL = 5000;

export const STATUS_LEGEND = {
  NOT_STARTED: 'purple',
  QUEUED: 'skyBlue',
  RUNNING: 'lightBlue',
  COMPLETED: 'green',
  FAILED: 'pink',
  CANCELED: 'orange',
};

export const STATUS_NAME_LEGEND = {
  NOT_STARTED: 'Not Started',
  QUEUED: 'In Queue',
  RUNNING: 'In Progress',
  COMPLETED: 'Succeeded',
  FAILED: 'Failed',
  CANCELED: 'Canceled',
};

export const STATUS_LONG_NAME_LEGEND = {
  NOT_STARTED: 'Not started',
  QUEUED: 'In the queue',
  RUNNING: 'In Progress',
  COMPLETED: 'Succeeded',
  FAILED: 'Failed',
  CANCELED: 'Canceled',
};

export const STATUS_PHRASE_LEGEND = {
  NOT_STARTED: 'not started',
  QUEUED: 'queued',
  RUNNING: 'started',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELED: 'canceled',
};

export const PIPELINE_STATES = {
  NOT_STARTED: 'NOT_STARTED',
  QUEUED: 'QUEUED',
  RUNNING: 'RUNNING',
  COMPLETED: 'COMPLETED',
  FAILED: 'FAILED',
  CANCELED: 'CANCELED',
};
