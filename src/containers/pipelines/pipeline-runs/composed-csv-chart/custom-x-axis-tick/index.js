import React from 'react';
import moment from 'moment';

import { Text, Rectangle } from 'recharts';

const CustomXAxisTick = (props) => {
  const {
    fill, x, y, payload, style, width, index, visibleTicksCount, isTimestamp,
  } = props;

  const tickValue = payload && (isTimestamp ? moment.unix(payload.value) : payload.value);

  const showTickRect = index !== (visibleTicksCount - 1) && index % 2;

  const rectWidth = width / (visibleTicksCount - 1);

  const dateOffset = isTimestamp ? 28 : 22;

  const dateFontSize = isTimestamp ? 10 : 12;

  return [
    isTimestamp && (
      <Text key="date" textAnchor="middle" fill={fill} x={x} y={y + 16} style={style} fontWeight={300} fontSize={12}>{tickValue.format('MMM D')}</Text>
    ),
    isTimestamp && (
      <Text key="time" textAnchor="middle" fill={fill} x={x} y={y + dateOffset} style={style} fontSize={dateFontSize}>{tickValue.format('h:mm A')}</Text>
    ),
    !isTimestamp && (
      <Text key="value" textAnchor="middle" fill={fill} x={x} y={y + 16} style={style} fontSize={12}>{tickValue}</Text>
    ),
    showTickRect && ( // y position is based off of chart container margin-top. height as well.
      <Rectangle key="tickrect" fill="rgba(196, 196, 196, 0.1)" fillOpacity={0.1} x={x} y={32} width={rectWidth} height={y - 34} style={style} />
    ),
  ];
};

export default CustomXAxisTick;
