import React from 'react';
import moment from 'moment';

import { Text } from 'recharts';

const CustomYAxisTick = (props) => {
  const {
    fill, x, y, payload, style, fontSize, isTimestamp,
  } = props;

  let tickValue = payload.value;

  if (isTimestamp) {
    tickValue = moment.unix(tickValue).format('MM/DD/YYYY h:mm A');
  }

  return [
    <Text textAnchor="middle" width={32} fill={fill} x={x - 32} y={y + 3} style={style} fontSize={fontSize}>{tickValue}</Text>,
  ];
};

export default CustomYAxisTick;
