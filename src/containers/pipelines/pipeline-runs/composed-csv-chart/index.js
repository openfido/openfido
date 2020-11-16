import React, { useEffect, useState } from 'react';
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

import { requestArtifact } from 'services';
import {
  chartTypes,
  dataTypes,
  dataScales,
  chartFills,
  chartStrokes,
  XAXIS,
  YAXIS,
} from 'config/charts';
import {
  parseCsvData,
  getLimitedDataPointsForGraph,
  axesFormatter,
} from 'util/charts';
import colors from 'styles/colors';
import CustomXAxisTick from './custom-x-axis-tick';
import CustomYAxisTick from './custom-y-axis-tick';

const ComposedCsvChart = ({
  type, config, height, artifact, sendChartData,
}) => {
  const axesComponents = [];
  const dataComponents = [];

  const [computedChartData, setComputedChartData] = useState(null);
  const [computedChartTypes, setComputedChartTypes] = useState({});
  const [computedChartScales, setComputedChartScales] = useState({});

  useEffect(() => {
    if (!computedChartData) {
      const useChartData = (data, types, scales) => {
        const limitedDataSet = getLimitedDataPointsForGraph({
          data,
          minIndex: 0,
          maxIndex: data.length - 1,
        });

        setComputedChartData(limitedDataSet);
        setComputedChartTypes(types);
        setComputedChartScales(scales);

        if (sendChartData) sendChartData(data);
      };

      requestArtifact(artifact) // uses fetch
        .then((response) => response.text())
        .then((data) => parseCsvData(data, useChartData));
    }
  }, [computedChartData, artifact, sendChartData]);

  if (config && config[XAXIS] && config[YAXIS] && chartFills && chartStrokes) {
    const axesByType = {
      [dataTypes.NUMBER]: [],
      [dataTypes.TIME]: [],
      [dataTypes.CATEGORY]: [],
    };

    config[YAXIS].forEach((axis, index) => {
      if (axis in computedChartTypes) {
        axesByType[computedChartTypes[axis]].push(axis);
      }

      switch (type) {
        case chartTypes.LINE_CHART: // TODO: toggle Area
          dataComponents.push((
            <Area
              key={`area${axis}`}
              dataKey={axis}
              yAxisId={computedChartTypes[axis]}
              dot={false}
              fill={chartFills[index]}
              stroke={chartStrokes[index]}
            />
          ));
          break;
        case chartTypes.BAR_CHART: // TODO: bar column legend
          dataComponents.push((
            <Bar
              key={`bar${axis}`}
              dataKey={axis}
              yAxisId={computedChartTypes[axis]}
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

    if (axesByType[dataTypes.NUMBER].length) { // use axesByType to get number y-axis
      axesComponents.push((
        <YAxis
          key="yAxisNumber"
          yAxisId={dataTypes.NUMBER}
          type={dataTypes.NUMBER}
          scale={computedChartScales[axesByType[dataTypes.NUMBER][0]] || dataScales.AUTO} // scale by first 'number' column scale setting
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
            value={axesByType[dataTypes.NUMBER].join(', ')}
            position="insideLeft"
            offset={-16}
            style={{
              textAnchor: 'middle', fontSize: 14, fontWeight: 'bold', fill: colors.gray,
            }}
          />
        </YAxis>
      ));
    }

    if (axesByType[dataTypes.TIME].length) { // use axesByType to get time y-axis
      axesComponents.push((
        <YAxis
          key="yAxisTime"
          yAxisId={dataTypes.TIME}
          type={dataTypes.NUMBER}
          scale={dataScales.TIME}
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

    if (axesByType[dataTypes.CATEGORY].length) { // use axesByType to get category y-axis
      axesComponents.push((
        <YAxis
          key="yAxisCategory"
          yAxisId={dataTypes.CATEGORY}
          type={dataTypes.CATEGORY}
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
            value={axesByType[dataTypes.CATEGORY].join(', ')}
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
      if (axis in computedChartTypes && axis in computedChartScales) {
        switch (computedChartTypes[axis]) {
          case dataTypes.TIME:
            axesComponents.push((
              <XAxis
                key={`xAxis${axis}`}
                dataKey={axis}
                type={dataTypes.NUMBER}
                scale={dataTypes.TIME}
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
          case dataTypes.NUMBER:
            axesComponents.push((
              <XAxis
                key={`xAxis${axis}`}
                dataKey={axis}
                type={dataTypes.NUMBER}
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
          case dataTypes.CATEGORY:
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
        data={computedChartData}
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

ComposedCsvChart.propTypes = {
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

ComposedCsvChart.defaultProps = {
  height: 264,
  sendChartData: null,
};

export default ComposedCsvChart;
