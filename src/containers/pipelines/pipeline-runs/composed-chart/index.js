import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import {
  ResponsiveContainer,
  ComposedChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Area,
  Bar,
  Label,
  Tooltip,
} from 'recharts';

import {
  CHART_TYPES, chartFills, chartStrokes, XAXIS, YAXIS,
} from 'config/charts';
import colors from 'styles/colors';
import CustomXAxisTick from './custom-x-axis-tick';
import CustomYAxisTick from './custom-y-axis-tick';

const TimeSeriesChart = ({
  type, config, height, chartData, chartTypes, chartScales,
}) => {
  const axesComponents = [];
  const dataComponents = [];

  const axesFormatter = (value) => {
    const valueString = value.toString();

    if (valueString.length === 10) {
      const dataValue = moment.unix(value);
      if (dataValue.isValid()) {
        return moment.unix(value).format('M/D/YYYY h:mm:ss A');
      }
    }

    if (valueString.match(/^-?[0-9]+([,.][0-9]+)?$/)) {
      return parseFloat(value).toFixed(4);
    }

    return value;
  };

  if (config && config[XAXIS] && config[YAXIS] && chartFills && chartStrokes) {
    const allNumberYAxes = [];

    config[YAXIS].forEach((axis, index) => {
      const isNumberType = chartTypes[axis] === 'number';

      if (axis in chartTypes && axis in chartScales) {
        switch (chartTypes[axis]) {
          case 'number':
            allNumberYAxes.push(axis);
            break;
          case 'time':
            axesComponents.push((
              <YAxis
                key={`yAxis${axis}`}
                yAxisId={`${axis}${index}`}
                scale={chartScales[axis] || 'time'}
                type="number"
                interval="preserveStartEnd"
                domain={['auto', 'auto']}
                fontSize={12}
                style={{ fontWeight: '500', fill: colors.gray10 }}
                tickLine={false}
                tickSize={0}
                tickCount={5}
                tick={<CustomYAxisTick isTimestamp />}
              />
            ));
            break;
          case 'category':
          default:
            axesComponents.push((
              <YAxis
                key={`yAxis${axis}`}
                yAxisId={`${axis}${index}`}
                type="category"
                domain={['high', 'low']}
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
                  value={axis}
                  position="insideLeft"
                  offset={-16}
                  style={{
                    textAnchor: 'middle', fontSize: 14, fontWeight: 'bold', fill: colors.gray,
                  }}
                />
              </YAxis>
            ));
            break;
        }
      }

      const yAxisId = isNumberType ? 'number' : `${axis}${index}`;

      switch (type) {
        case CHART_TYPES.LINE_CHART: // TODO: toggle Area
          dataComponents.push((
            <Area
              key={`area${axis}`}
              dataKey={axis}
              yAxisId={yAxisId}
              dot={false}
              fill={chartFills[index]}
              stroke={chartStrokes[index]}
            />
          ));
          break;
        case CHART_TYPES.BAR_CHART: // TODO: bar column legend
          dataComponents.push((
            <Bar
              key={`bar${axis}`}
              dataKey={axis}
              yAxisId={yAxisId}
              dot={false}
              fill={chartFills[index]}
              stroke={chartStrokes[index]}
            />
          ));
          break;
        default:
          break;
      }
    });

    if (allNumberYAxes.length) {
      axesComponents.push((
        <YAxis
          key="yAxisNumber"
          type="number"
          scale={chartScales[allNumberYAxes[0]] || 'auto'}
          interval={0}
          yAxisId="number"
          fontSize={12}
          style={{ fontWeight: '500', fill: colors.gray10 }}
          angle={-90}
          tickLine={false}
          tickSize={0}
          tickCount={5}
          tick={<CustomYAxisTick isNumber />}
          stroke={colors.gray10}
          allowDecimals
        >
          <Label
            angle={-90}
            value={allNumberYAxes.join(', ')}
            position="insideLeft"
            offset={-16}
            style={{
              textAnchor: 'middle', fontSize: 14, fontWeight: 'bold', fill: colors.gray,
            }}
          />
        </YAxis>
      ));
    }

    config[XAXIS].forEach((axis) => {
      // TODO add a label for the YAxis.
      if (axis in chartTypes && axis in chartScales) {
        switch (chartTypes[axis]) {
          case 'time':
            axesComponents.push((
              <XAxis
                key={`xAxis${axis}`}
                dataKey={axis}
                type="number"
                scale="time"
                interval="preserveStartEnd"
                domain={['auto', 'auto']}
                fontSize={10}
                style={{ fontWeight: '500', fill: colors.gray10 }}
                tickLine={false}
                tickSize={0}
                tick={<CustomXAxisTick isTimestamp />}
              />
            ));
            break;
          case 'number':
            axesComponents.push((
              <XAxis
                key={`xAxis${axis}`}
                dataKey={axis}
                type="number"
                interval="preserveStartEnd"
                domain={['auto', 'auto']}
                fontSize={10}
                style={{ fontWeight: '500', fill: colors.gray10 }}
                tickLine={false}
                tickSize={0}
                stroke={colors.gray10}
                tick={CustomXAxisTick}
              />
            ));
            break;
          case 'category':
          default:
            axesComponents.push((
              <XAxis
                key={`xAxis${axis}`}
                dataKey={axis}
                interval="preserveStartEnd"
                fontSize={10}
                style={{ fontWeight: '500', fill: colors.gray10 }}
                tickLine={false}
                tickSize={0}
                stroke={colors.gray10}
                tick={CustomXAxisTick}
              />
            ));
            break;
        }
      }
    });
  }

  return (
    <ResponsiveContainer
      width="100%"
      height={height}
    >
      <ComposedChart
        height={height}
        data={chartData}
        margin={{
          bottom: 16,
          left: 32,
          right: 32,
        }}
      >
        <CartesianGrid stroke="rgba(112, 112, 112, 0.2)" vertical={false} />
        {axesComponents}
        {dataComponents}
        <Tooltip
          labelFormatter={axesFormatter}
          formatter={axesFormatter}
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
};

TimeSeriesChart.propTypes = {
  type: PropTypes.string.isRequired,
  config: PropTypes.shape({
    [XAXIS]: PropTypes.arrayOf(PropTypes.string).isRequired,
    [YAXIS]: PropTypes.arrayOf(PropTypes.string).isRequired,
  }).isRequired,
  height: PropTypes.number,
  chartData: PropTypes.any.isRequired,
  chartTypes: PropTypes.any.isRequired,
  chartScales: PropTypes.any.isRequired,
};

TimeSeriesChart.defaultProps = {
  height: 264,
};

export default TimeSeriesChart;
