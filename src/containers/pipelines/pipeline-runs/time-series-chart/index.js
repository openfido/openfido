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

import { requestArtifact } from 'services';
import {
  chartTypes, mockData, chartFills, chartStrokes, XAXIS, YAXIS,
} from 'config/charts';
import { parseCsvData } from 'util/charts';
import colors from 'styles/colors';
import CustomXAxisTick from './custom-x-axis-tick';
import CustomYAxisTick from './custom-y-axis-tick';

const TimeSeriesChart = ({
  type, config, height, artifact, sendChartData,
}) => {
  const axesComponents = [];
  const dataComponents = [];

  const [chartData, setChartData] = useState(null);

  const useChartData = (data) => {
    setChartData(data);

    if (sendChartData) sendChartData(data);
  };

  useEffect(() => {
    if (!chartData) {
      parseCsvData(mockData, useChartData); // TODO: remove mock CSV data

      requestArtifact(artifact)
        .then((response) => {
          parseCsvData(response.data, useChartData);
        });
    }
  }, [chartData, artifact, useChartData]);

  if (config && config[XAXIS] && config[YAXIS] && chartFills && chartStrokes) {
    config[YAXIS].forEach((axis, index) => {
      switch (true) {
        case /.\d/.test(axis): // tariff - Energy Used (kWh)
          axesComponents.push((
            <YAxis
              key={`yAxis${axis}`}
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
          ));
          break;
        default:
          break;
      }

      switch (type) {
        case chartTypes.LINE_CHART: // TODO: toggle Area
          dataComponents.push(<Area key={`area${axis}`} dataKey={axis} dot={false} fill={chartFills[index]} stroke={chartStrokes[index]} />);
          break;
        case chartTypes.BAR_CHART: // TODO: bar column legend
          dataComponents.push(<Bar key={`bar${axis}`} dataKey={axis} dot={false} fill={chartFills[index]} stroke={chartStrokes[index]} />);
          break;
        default:
          break;
      }
    });

    config[XAXIS].forEach((axis) => {
      switch (axis) {
        case 'datetime':
          axesComponents.push((
            <XAxis
              key={`xAxis${axis}`}
              dataKey={axis}
              scale="time"
              type="number"
              interval="preserveStart"
              domain={['auto', 'auto']}
              fontSize={10}
              style={{ fontWeight: '500', fill: colors.gray10 }}
              tickLine={false}
              tickSize={0}
              tick={CustomXAxisTick}
            />
          ));
          break;
        default:
          axesComponents.push((
            <XAxis
              key={`xAxis${axis}`}
              dataKey={axis}
              fontSize={10}
              style={{ fontWeight: '500', fill: colors.gray10 }}
              tickLine={false}
              tickSize={0}
              stroke={colors.gray10}
            />
          ));
          break;
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
};

TimeSeriesChart.propTypes = {
  type: PropTypes.string.isRequired,
  config: PropTypes.shape({
    [XAXIS]: PropTypes.arrayOf(PropTypes.string).isRequired,
    [YAXIS]: PropTypes.arrayOf(PropTypes.string).isRequired,
  }).isRequired,
  artifact: PropTypes.shape({
    name: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
    uuid: PropTypes.string.isRequired,
  }).isRequired,
  height: PropTypes.number,
  sendChartData: PropTypes.func,
};

TimeSeriesChart.defaultProps = {
  height: 264,
  sendChartData: null,
};

export default TimeSeriesChart;
