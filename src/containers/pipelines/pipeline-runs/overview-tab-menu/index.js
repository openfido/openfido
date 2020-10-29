import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import { OVERVIEW_TAB, DATA_VISUALIZATION_TAB, CONSOLE_OUTPUT_TAB } from 'config/pipeline-runs';
import { StyledButton } from 'styles/app';
import colors from 'styles/colors';

const StyledOverviewTabMenu = styled.ul`
  list-style-type: none;
  padding: 0;
  display: grid;
  grid-gap: 32px;
  grid-gap: 2rem;
  grid-auto-flow: column;
  justify-content: start;
  li {
    padding-bottom: 4px;
    padding-bottom: 0.25rem;
    button {
      color: ${colors.gray};
      font-size: 16px;
      font-size: 1rem;
      line-height: 19px;
      line-height: 1.1875rem;
    }
    &.active {
      button {
        color: ${colors.lightBlue};
      }
      border-bottom: 1px solid ${colors.lightBlue};
    }
  }
`;

const OverviewTabMenu = ({ displayTab, setDisplayTab }) => (
  <StyledOverviewTabMenu mode="horizontal">
    <li className={displayTab === OVERVIEW_TAB ? 'active' : ''}>
      <StyledButton type="text" size="middle" onClick={() => setDisplayTab(OVERVIEW_TAB)}>
        Overview
      </StyledButton>
    </li>
    <li className={displayTab === DATA_VISUALIZATION_TAB ? 'active' : ''}>
      <StyledButton type="text" size="middle" onClick={() => setDisplayTab(DATA_VISUALIZATION_TAB)}>
        Data Visualization
      </StyledButton>
    </li>
    <li className={displayTab === CONSOLE_OUTPUT_TAB ? 'active' : ''}>
      <StyledButton type="text" size="middle" onClick={() => setDisplayTab(CONSOLE_OUTPUT_TAB)}>
        Console Output
      </StyledButton>
    </li>
  </StyledOverviewTabMenu>
);

OverviewTabMenu.propTypes = {
  displayTab: PropTypes.string.isRequired,
  setDisplayTab: PropTypes.func.isRequired,
};

export default OverviewTabMenu;
