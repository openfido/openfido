import React from 'react';
import { generatePath } from 'react-router';
import { NavLink } from 'react-router-dom';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import { StyledButton } from 'styles/app';
import colors from 'styles/colors';
import {
  ROUTE_PIPELINE_RUNS,
  ROUTE_PIPELINE_RUNS_CONSOLE_OUTPUT,
  ROUTE_PIPELINE_RUNS_DATA_VISUALIZATION,
} from 'config/routes';

const StyledOverviewTabMenu = styled.ul`
  list-style-type: none;
  padding: 0;
  display: grid;
  grid-gap: 32px;
  grid-gap: 2rem;
  grid-auto-flow: column;
  justify-content: start;
  li a {
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

const OverviewTabMenu = ({
  dataVisualizationReady, consoleOutputReady, pipelineInView, pipelineRunSelectedUuid,
}) => {
  const routeParams = {
    pipeline_uuid: pipelineInView,
    pipeline_run_uuid: pipelineRunSelectedUuid,
  };

  return (
    <StyledOverviewTabMenu mode="horizontal">
      <li>
        <NavLink exact to={generatePath(ROUTE_PIPELINE_RUNS, routeParams)}>
          <StyledButton type="text" size="middle">
            Overview
          </StyledButton>
        </NavLink>
      </li>
      {dataVisualizationReady && (
      <li>
        <NavLink exact to={generatePath(ROUTE_PIPELINE_RUNS_DATA_VISUALIZATION, routeParams)}>
          <StyledButton type="text" size="middle">
            Data Visualization
          </StyledButton>
        </NavLink>
      </li>
      )}
      {consoleOutputReady && (
      <li>
        <NavLink exact to={generatePath(ROUTE_PIPELINE_RUNS_CONSOLE_OUTPUT, routeParams)}>
          <StyledButton type="text" size="middle">
            Console Output
          </StyledButton>
        </NavLink>
      </li>
      )}
    </StyledOverviewTabMenu>
  );
};

OverviewTabMenu.propTypes = {
  dataVisualizationReady: PropTypes.bool,
  consoleOutputReady: PropTypes.bool,
  pipelineInView: PropTypes.string.isRequired,
  pipelineRunSelectedUuid: PropTypes.string.isRequired,
};

OverviewTabMenu.defaultProps = {
  dataVisualizationReady: false,
  consoleOutputReady: false,
};

export default OverviewTabMenu;
