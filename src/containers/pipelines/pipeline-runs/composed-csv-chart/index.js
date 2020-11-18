import React from 'react';
import PropTypes from 'prop-types';
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
  CHART_TYPES,
  DATA_TYPES,
  DATA_SCALES,
  chartFills,
  chartStrokes,
  XAXIS,
  YAXIS,
} from 'config/charts';
import { axesFormatter } from 'util/charts';
import colors from 'styles/colors';
import CustomXAxisTick from './custom-x-axis-tick';
import CustomYAxisTick from './custom-y-axis-tick';

const ComposedCsvChart = ({
  type, config, height, chartData, chartTypes, chartScales,
}) => {
  const axesComponents = [];
  const dataComponents = [];

  let hasTimeXAxis = false; // used for axesFormatter in util/charts

  if (config && config[XAXIS] && config[YAXIS] && chartFills && chartStrokes) {
    const axesByType = {
      [DATA_TYPES.NUMBER]: [],
      [DATA_TYPES.TIME]: [],
      [DATA_TYPES.CATEGORY]: [],
    };

    config[YAXIS].forEach((axis, index) => {
      if (axis in chartTypes) {
        axesByType[chartTypes[axis]].push(axis);
      }

      switch (type) {
        case CHART_TYPES.LINE_CHART: // TODO: toggle Area
          dataComponents.push((
            <Area
              key={`area${axis}`}
              dataKey={axis}
              yAxisId={chartTypes[axis]}
              dot={false}
              fill={chartFills[index]}
              stroke={chartStrokes[index]}
              formatter={(value) => axesFormatter(value, chartTypes[axis] === DATA_TYPES.TIME)}
            />
          ));
          break;
        case CHART_TYPES.BAR_CHART: // TODO: bar column legend
          dataComponents.push((
            <Bar
              key={`bar${axis}`}
              dataKey={axis}
              yAxisId={chartTypes[axis]}
              dot={false}
              fill={chartFills[index]}
              stroke={chartStrokes[index]}
              formatter={(value) => axesFormatter(value, chartTypes[axis] === DATA_TYPES.TIME)}
            />
          ));
          break;
        default:
          break;
      }
    });

    if (axesByType[DATA_TYPES.NUMBER].length) { // use axesByType to get number y-axis
      axesComponents.push((
        <YAxis
          key="yAxisNumber"
          yAxisId={DATA_TYPES.NUMBER}
          type={DATA_TYPES.NUMBER}
          scale={chartScales[axesByType[DATA_TYPES.NUMBER][0]] || DATA_SCALES.AUTO} // scale by first 'number' column scale setting
          interval={0}
          fontSize={12}
          style={{ fontWeight: 500, fill: colors.gray10 }}
          angle={-90}
          tickLine={false}
          tickSize={0}
          tickCount={5}
          tick={<CustomYAxisTick isNumber />}
          stroke={colors.gray10}
        >
          <Label
            angle={-90}
            value={axesByType[DATA_TYPES.NUMBER].join(', ')}
            position="insideLeft"
            offset={-16}
            style={{
              textAnchor: 'middle', fontSize: 14, fontWeight: 'bold', fill: colors.gray,
            }}
          />
        </YAxis>
      ));
    }

    if (axesByType[DATA_TYPES.TIME].length) { // use axesByType to get time y-axis
      axesComponents.push((
        <YAxis
          key="yAxisTime"
          yAxisId={DATA_TYPES.TIME}
          type={DATA_TYPES.NUMBER}
          scale={DATA_SCALES.TIME}
          interval="preserveStartEnd"
          domain={['auto', 'auto']}
          fontSize={12}
          style={{ fontWeight: 500, fill: colors.gray10 }}
          tickLine={false}
          tickSize={0}
          tickCount={5}
          stroke={colors.gray10}
          tick={<CustomYAxisTick isTimestamp />}
        />
      ));
    }

    if (axesByType[DATA_TYPES.CATEGORY].length) { // use axesByType to get category y-axis
      axesComponents.push((
        <YAxis
          key="yAxisCategory"
          yAxisId={DATA_TYPES.CATEGORY}
          type={DATA_TYPES.CATEGORY}
          interval="preserveStartEnd"
          fontSize={12}
          style={{ fontWeight: 500, fill: colors.gray10 }}
          angle={-90}
          tickLine={false}
          tickSize={0}
          tickCount={5}
          stroke={colors.gray10}
          tick={CustomYAxisTick}
        >
          <Label
            angle={-90}
            value={axesByType[DATA_TYPES.CATEGORY].join(', ')}
            position="insideLeft"
            offset={-16}
            style={{
              textAnchor: 'middle', fontSize: 14, fontWeight: 'bold', fill: colors.gray,
            }}
          />
        </YAxis>
      ));
    }

    config[XAXIS].forEach((axis) => { // currently only 1 x-axis allowed to be picked, in config-chart-step component
      if (axis in chartTypes && axis in chartScales) {
        switch (chartTypes[axis]) {
          case DATA_TYPES.TIME:
            hasTimeXAxis = true;
            axesComponents.push((
              <XAxis
                key={`xAxis${axis}`}
                dataKey={axis}
                type={DATA_TYPES.NUMBER}
                scale={DATA_SCALES.TIME}
                interval="preserveStartEnd"
                domain={['auto', 'auto']}
                fontSize={10}
                style={{ fontWeight: '500', fill: colors.gray10 }}
                tickLine={false}
                tickSize={0}
                stroke={colors.gray10}
                tick={<CustomXAxisTick isTimestamp />}
              />
            ));
            break;
          case DATA_TYPES.NUMBER:
            axesComponents.push((
              <XAxis
                key={`xAxis${axis}`}
                dataKey={axis}
                type={DATA_TYPES.NUMBER}
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
          case DATA_TYPES.CATEGORY:
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
          labelFormatter={(value) => axesFormatter(value, hasTimeXAxis)}
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

ComposedCsvChart.propTypes = {
  type: PropTypes.string.isRequired,
  config: PropTypes.shape({
    [XAXIS]: PropTypes.arrayOf(PropTypes.string).isRequired,
    [YAXIS]: PropTypes.arrayOf(PropTypes.string).isRequired,
  }).isRequired,
  height: PropTypes.number,
  chartData: PropTypes.arrayOf(PropTypes.object).isRequired,
  chartTypes: PropTypes.objectOf(PropTypes.string).isRequired,
  chartScales: PropTypes.objectOf(PropTypes.string).isRequired,
};

ComposedCsvChart.defaultProps = {
  height: 264,
};

export default ComposedCsvChart;
