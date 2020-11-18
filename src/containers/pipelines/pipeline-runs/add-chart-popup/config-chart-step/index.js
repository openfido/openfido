import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Dropdown, Space } from 'antd';
import styled from 'styled-components';

import {
  XAXIS, YAXIS, AXES_LIMIT, CHART_TITLE_LENGTH_LIMIT,
} from 'config/charts';
import CloseOutlined from 'icons/CloseOutlined';
import { PopupButton } from 'styles/pipeline-runs';
import {
  StyledInput, StyledText, StyledMenu, StyledMenuItem, StyledButton,
} from 'styles/app';
import colors from 'styles/colors';
import ComposedCsvChart from '../../composed-csv-chart';

const ConfigChartForm = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 570px;
  section {
    border-radius: 6px;
    background-color: ${colors.white};
    min-height: 231px;
    padding: 2rem 0 0 1rem;
  }
  > button {
    margin: 24px auto 0 auto;
    margin: 1.5rem auto 0 auto;
  }
  input.invalid {
    &::placeholder {
      color: ${colors.pink};
    }
  }
`;

const AxisItem = styled.div`
  background-color ${colors.white};
  color: ${colors.darkText};
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px 4px 12px;
  padding: 0.25rem 0.5rem 0.25rem 0.75rem;
  margin-top: 16px;
  margin-top: 1rem;
  font-size: 16px;
  line-height: 19px;
  width: 261px;
  height: 48px;
  max-height: 48px;
  cursor: pointer;
  position: relative;
  .anticon {
    position: static;
    float: right;
    svg {
      width: 18px;
      width: 1.125rem;
      height: 18px;
      height: 1.125rem;
    }
  }
  &:hover {
    .anticon svg line {
      stroke: ${colors.gray20};
    }
  }
`;

const AxesList = styled.div`
  display: flex;
  justify-content: space-between;
  > div {
    width: 261px;
  }
`;

const ColumnMenu = styled(StyledMenu)`
  max-height: 200px;
  overflow-y: overlay;
`;

const ColumnLabel = styled(StyledText)`
  margin-right: 24px;
  margin-right: 1.5rem;
  white-space: pre;
`;

const ColumnName = styled.span`
  margin-right: 8px;
  margin-right: 0.5rem;
  white-space: pre;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const ConfigChartStep = ({
  chartType, onNextClicked, chartData, chartTypes, chartScales,
}) => {
  const [xAxis, setXAxis] = useState([]);
  const [yAxis, setYAxis] = useState([]);
  const [title, setTitle] = useState('');
  const [titleError, setTitleError] = useState(false);

  const chartConfig = {
    [XAXIS]: xAxis,
    [YAXIS]: yAxis,
  };

  const onAddChartClicked = () => {
    if (title && title.length && title.length < CHART_TITLE_LENGTH_LIMIT) {
      onNextClicked(title, chartConfig);
      setTitleError(false);
    } else {
      setTitleError(true);
    }
  };

  const addAxis = (axis, setAxis, item, replace) => {
    if (axis.length < AXES_LIMIT) {
      if (replace) {
        setAxis([item]);
      } else {
        const axes = axis.filter((axisItem) => axisItem !== item);
        axes.push(item);
        setAxis(axes);
      }
    }
  };

  const removeAxis = (axis, setAxis, item) => {
    const axes = axis.filter((axisItem) => axisItem !== item);
    setAxis(axes);
  };

  const xAxisMenu = (
    <ColumnMenu>
      {chartData && chartData.length && Object.keys(chartData[0]).map((axis) => (
        <StyledMenuItem
          bordercolor="lightBg"
          hoverbgcolor="darkGray"
          hovercolor="white"
          onClick={() => addAxis(xAxis, setXAxis, axis, true)}
        >
          <span>{axis}</span>
        </StyledMenuItem>
      ))}
      {(!chartData || !chartData.length) && (
        <StyledText color="darkGray">No options available.</StyledText>
      )}
    </ColumnMenu>
  );

  const yAxisMenu = (
    <ColumnMenu>
      {chartData && chartData.length && Object.keys(chartData[0]).map((axis) => (
        <StyledMenuItem
          bordercolor="lightBg"
          hoverbgcolor="darkGray"
          hovercolor="white"
          onClick={() => addAxis(yAxis, setYAxis, axis)}
        >
          <span>{axis}</span>
        </StyledMenuItem>
      ))}
      {(!chartData || !chartData.length) && (
        <StyledText color="darkGray">No options available.</StyledText>
      )}
    </ColumnMenu>
  );

  return (
    <ConfigChartForm>
      <Space direction="vertical" size={16}>
        <StyledInput
          size="middle"
          placeholder="Edit Name of Chart"
          bgcolor="white"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className={titleError && 'invalid'}
        />
        <section>
          <ComposedCsvChart
            type={chartType}
            config={chartConfig}
            height={231}
            chartData={chartData}
            chartTypes={chartTypes}
            chartScales={chartScales}
          />
        </section>
        <AxesList>
          <div>
            <Space size={8}>
              <strong>
                X-axis
              </strong>
              <Dropdown overlay={xAxisMenu}>
                <StyledButton type="text" size="small" color="transparent">
                  + Add Column
                </StyledButton>
              </Dropdown>
            </Space>
            {xAxis && xAxis.map((axisItem) => (
              <AxisItem key={axisItem} title={axisItem}>
                <ColumnName>{axisItem}</ColumnName>
                <CloseOutlined color="lightGray" onClick={() => removeAxis(xAxis, setXAxis, axisItem)} />
              </AxisItem>
            ))}
            {!xAxis.length && (
              <AxisItem>
                <StyledText color="lightGray">Add X-axis</StyledText>
              </AxisItem>
            )}
          </div>
          <div>
            <Space size={8}>
              <strong>
                Y-axis
              </strong>
              <Dropdown overlay={yAxisMenu}>
                <StyledButton type="text" size="small" color="transparent">
                  + Add Column
                </StyledButton>
              </Dropdown>
            </Space>
            {yAxis && yAxis.map((axisItem, axisIndex) => (
              <AxisItem key={axisItem} title={axisItem}>
                <ColumnLabel color="lightGray" fontweight={500} className="columnLabel">
                  {`Column ${axisIndex + 1}`}
                </ColumnLabel>
                <ColumnName className="columnName">{axisItem}</ColumnName>
                <CloseOutlined color="lightGray" onClick={() => removeAxis(yAxis, setYAxis, axisItem)} />
              </AxisItem>
            ))}
            {!yAxis.length && (
              <AxisItem>
                <StyledText color="lightGray">Add Y-axis</StyledText>
              </AxisItem>
            )}
          </div>
        </AxesList>
      </Space>
      <PopupButton size="middle" color="blue" width={108} onClick={onAddChartClicked}>
        Add Chart
      </PopupButton>
    </ConfigChartForm>
  );
};

ConfigChartStep.propTypes = {
  selectedArtifact: PropTypes.shape({
    name: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
    uuid: PropTypes.string.isRequired,
  }).isRequired,
  onNextClicked: PropTypes.func.isRequired,
  chartType: PropTypes.string.isRequired,
  chartData: PropTypes.arrayOf({ }).isRequired,
  chartTypes: PropTypes.arrayOf(PropTypes.string).isRequired,
  chartScales: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default ConfigChartStep;
