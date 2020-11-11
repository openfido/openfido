import React from 'react';
import moment from 'moment';
import {
  ResponsiveContainer,
  ComposedChart,
  XAxis,
  YAxis,
  Area,
  CartesianGrid,
  Label,
  Tooltip,
} from 'recharts';

import { mockData } from 'config/charts';
import colors from 'styles/colors';
import CustomXAxisTick from './custom-x-axis-tick';
import CustomYAxisTick from './custom-y-axis-tick';

const LineChart = () => (
  <ResponsiveContainer
    width="100%"
    height={264}
  >
    <ComposedChart
      width={1000}
      height={264}
      data={mockData}
      margin={{
        bottom: 16,
        left: 32,
        right: 32,
      }}
    >
      <CartesianGrid stroke="rgba(112, 112, 112, 0.2)" vertical={false} />
      <XAxis
        dataKey="timestamp"
        scale="time"
        type="number"
        interval="preserveStart"
        domain={['auto', 'auto']}
        fontSize={10}
        style={{ fontWeight: '500', fill: colors.gray10 }}/*
          label={{
            'L1': 'DateTime', position: 'insideBottom', offset: -32, fill: colors.gray,
          }} */
        tickLine={false}
        tickSize={0}
        tick={CustomXAxisTick}
        stroke={colors.gray10}
      />
      <YAxis
        type="number"
        interval="preserveStartEnd"
        fontSize={12}
        style={{ fontWeight: '500', fill: colors.gray10 }}
        angle={-90}
        tickLine={false}
        tickSize={0}
        tickCount={5}
        tick={CustomYAxisTick}
        stroke={colors.gray10}
      >
        <Label
          angle={-90}
          value="Energy Used (kWh)"
          position="insideLeft"
          offset={-16}
          style={{
            textAnchor: 'middle', fontSize: 14, fontWeight: 'bold', fill: colors.gray,
          }}
        />
      </YAxis>
      <Area dataKey="L4" dot={false} fill={colors.chartBlue} stroke={colors.chartBlue} />
      <Area dataKey="L3" dot={false} fill={colors.chartGray} stroke={colors.chartGrayStroke} />
      <Area dataKey="L2" dot={false} fill={colors.chartGreen} stroke={colors.chartGreen} />
      <Area dataKey="L1" dot={false} fill={colors.chartYellow} stroke={colors.chartYellow} />
      <Tooltip
        labelFormatter={(value) => moment.unix(value).format('M/D/YYYY h:mm:ss A')}
        contentStyle={{
          fontSize: 12,
          fontWeight: 400,
          lineHeight: '14px',
        }}
        labelStyle={{
          fontSize: 12,
          fontWeight: 'bold',
          lineHeight: '20px',
          color: colors.gray,
        }}
        cursor={{ stroke: colors.gray, strokeWidth: 1, strokeDasharray: '3, 3' }}
      />
    </ComposedChart>
  </ResponsiveContainer>
);

export default LineChart;
