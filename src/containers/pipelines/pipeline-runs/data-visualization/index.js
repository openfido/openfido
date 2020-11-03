import React, { useState } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import { DATA_VISUALIZATION_TAB } from 'config/pipeline-runs';
import { StyledH2, StyledButton } from 'styles/app';
import colors from 'styles/colors';
import OverviewTabMenu from '../overview-tab-menu';
import AddChartPopup from '../add-chart-popup';

const StyledDataVisualization = styled.div`
  padding: 16px 20px;
  padding: 1rem 1.25rem;
  header {
    display: flex;
    h2 {
      margin-right: 4px;
      margin-right: 0.25rem;
      width: 108px;
    }
    ul {
      margin-top: 3px;
      margin-top: 0.1875rem;
    }
  }
  section {
    margin-top: 16px;
    margin-top: 1rem;
    background-color: ${colors.white};
    color: ${colors.black};
    border-radius: 6px;
    max-width: 972px;
    font-size: 18px;
    font-size: 1.125rem;
    line-height: 21px;
    line-height: 1.3125rem;
    padding: 42px 28px;
    padding: 2.625rem 1.75rem;
  }
`;

const DataVisualization = ({ pipelineInView, sequence, setDisplayTab }) => {
  const [showAddChartPopup, setShowAddChartPopup] = useState(true);

  return (
    <>
      <StyledDataVisualization>
        <header>
          <StyledH2 color="black">
            Run #
            {sequence}
          </StyledH2>
          <OverviewTabMenu displayTab={DATA_VISUALIZATION_TAB} setDisplayTab={setDisplayTab} />
        </header>
        <StyledButton color="white" onClick={() => setShowAddChartPopup(true)}>+ Add A Chart</StyledButton>
        <section>
          graph
        </section>
      </StyledDataVisualization>
      {showAddChartPopup && (
        <AddChartPopup
          handleOk={() => setShowAddChartPopup(false)}
          handleCancel={() => setShowAddChartPopup(false)}
          artifacts={(pipelineInView && pipelineInView.artifacts) || [{ name: 'artifact.png' }, { name: 'data.csv' }]}
        />
      )}
    </>
  );
};

DataVisualization.propTypes = {
  pipelineInView: PropTypes.string.isRequired,
  sequence: PropTypes.number.isRequired,
  setDisplayTab: PropTypes.func.isRequired,
};

export default DataVisualization;
