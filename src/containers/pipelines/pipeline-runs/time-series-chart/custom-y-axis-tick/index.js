import React from 'react';

import { Text } from 'recharts';

const CustomYAxisTick = (props) => {
  const {
    fill, x, y, payload, style, fontSize,
  } = props;

  const tickValue = payload.value;

  return [
    <Text textAnchor="middle" width={32} fill={fill} x={x - 32} y={y + 3} style={style} fontSize={fontSize}>{tickValue}</Text>,
  ];
};

export default CustomYAxisTick;
