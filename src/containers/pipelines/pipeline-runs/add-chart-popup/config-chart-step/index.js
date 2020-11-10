import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import CloseOutlined from 'icons/CloseOutlined';
import { PopupButton } from 'styles/pipeline-runs';
import { StyledInput, StyledText } from 'styles/app';
import colors from 'styles/colors';

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
  span:first-child {
    margin-right: 8px;
    margin-right: 0.5rem;
    white-space: pre;
    overflow: hidden;
    text-overflow: ellipsis;
  }
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
`;

const ConfigChartStep = ({ onNextClicked, chartType }) => {
  const onXAxisRemoveClicked = () => {

  };

  return (
    <form>
      <StyledInput size="middle" placeholder="Edit Name of Chart" bgcolor="white" />
      <section>
        {chartType}
      </section>
      <AxesList>
        <div>
          <strong>
            X-axis
          </strong>
          <AxisItem title="DateTime">
            <StyledText>DateTime</StyledText>
            <CloseOutlined color="lightGray" onClick={() => onXAxisRemoveClicked()} />
          </AxisItem>
        </div>
        <div>
          <strong>
            Y-axis
          </strong>
          <AxisItem title="DateTime">
            <StyledText>L1</StyledText>
            <CloseOutlined color="lightGray" onClick={() => onXAxisRemoveClicked()} />
          </AxisItem>
          <AxisItem title="DateTime">
            <StyledText>L2</StyledText>
            <CloseOutlined color="lightGray" onClick={() => onXAxisRemoveClicked()} />
          </AxisItem>
        </div>
      </AxesList>
      <PopupButton size="middle" color="blue" width={108} onClick={onNextClicked}>
        Add Chart
      </PopupButton>
    </form>
  );
};

ConfigChartStep.propTypes = {
  onNextClicked: PropTypes.func.isRequired,
  chartType: PropTypes.string.isRequired,
};

export default ConfigChartStep;
