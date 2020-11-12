import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import { chartTypes } from 'config/charts';
import { PopupButton } from 'styles/pipeline-runs';
import { StyledButton, StyledH4 } from 'styles/app';
import colors from 'styles/colors';
import LinesImg from './images/lines.svg';
import BarsImg from './images/bars.svg';

const ChartTypesList = styled.ul`
  list-style-type: none;
  padding: 0;
  margin: 12px 0;
  margin: 0.75rem 0;
  display: grid;
  justify-content: center;
  grid-auto-flow: column;
  grid-gap: 46px;
  grid-gap: 2.875rem;
  li {
   button.ant-btn {
     width: 178px;
     height: 178px;
     padding: 28px 8px;
     padding: 1.75rem 0.5rem;
     flex-wrap: wrap;
     border: 3px solid ${colors.white};
     border-radius: 2px;
     &, &:hover {
       background-color: ${colors.white};
     }
     &:active, &:focus {
       border: 3px solid ${colors.lightBlue};
       background-color: ${colors.white};
     }
   }
  }
`;

const SelectChartTypeStep = ({ onNextClicked, setChartType }) => {
  const onChartTypeSelected = () => onNextClicked();

  return (
    <form>
      <StyledH4 color="darkText">Select a chart type</StyledH4>
      <ChartTypesList>
        <li>
          <StyledButton type="text" size="middle" textcolor="darkText" onClick={() => setChartType(chartTypes.LINE_CHART)}>
            Line Chart
            <img src={LinesImg} alt="Line" />
          </StyledButton>
        </li>
        <li>
          <StyledButton type="text" size="middle" textcolor="darkText" onClick={() => setChartType(chartTypes.BAR_CHART)}>
            Bar Chart
            <img src={BarsImg} alt="Bar" />
          </StyledButton>
        </li>
      </ChartTypesList>
      <PopupButton size="middle" color="blue" width={108} onClick={onChartTypeSelected}>
        Next
      </PopupButton>
    </form>
  );
};

SelectChartTypeStep.propTypes = {
  onNextClicked: PropTypes.func.isRequired,
  setChartType: PropTypes.func.isRequired,
};

export default SelectChartTypeStep;
