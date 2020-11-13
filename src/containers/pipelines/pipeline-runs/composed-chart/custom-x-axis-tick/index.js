import React from 'react';
import moment from 'moment';

import { Text, Rectangle } from 'recharts';

const CustomXAxisTick = (props) => {
  const {
    fill, x, y, payload, style, width, index, visibleTicksCount, isTimestamp,
  } = props;

  const tickValue = payload && (isTimestamp ? moment.unix(payload.value) : payload.value);

  const showTickRect = index !== (visibleTicksCount - 1) && index % 2;

  const rectWidth = width / visibleTicksCount;

  const showMonth = payload && (
    !moment.unix(payload.value).startOf('month').diff(tickValue)
      || !moment.unix(payload.value).endOf('month').diff(tickValue)
  );

  const dateOffset = showMonth ? 28 : 22;

  const dateFontSize = showMonth ? 10 : 12;

  return [
    showMonth && isTimestamp && (
      <Text textAnchor="middle" fill={fill} x={x} y={y + 16} style={style} fontWeight={300} fontSize={12}>{tickValue.format('MMM')}</Text>
    ),
    isTimestamp && (
      <Text textAnchor="middle" fill={fill} x={x} y={y + dateOffset} style={style} fontSize={dateFontSize}>{tickValue.format('D')}</Text>
    ),
    !isTimestamp && (
      <Text textAnchor="middle" fill={fill} x={x} y={y + 16} style={style} fontSize={12}>{tickValue}</Text>
    ),
    showTickRect && <Rectangle fill="rgba(196, 196, 196, 0.1)" fillOpacity={0.1} x={x} y={0} width={rectWidth} height={y - 2} style={style} />,
  ];
};

export default CustomXAxisTick;
