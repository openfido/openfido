import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useSelector } from 'react-redux';
import styled from 'styled-components';

import { requestPipelineRunConsoleOutput } from 'services';
import { CONSOLE_OUTPUT_TAB } from 'config/pipeline-runs';
import { StyledH2, StyledH5 } from 'styles/app';
import colors from 'styles/colors';
import OverviewTabMenu from '../overview-tab-menu';

const StyledConsoleOutput = styled.div`
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

const ConsoleOutput = ({
  pipelineInView, pipelineRunSelectedUuid, sequence, setDisplayTab,
}) => {
  const [stdout, setStdout] = useState();
  const [stderr, setStderr] = useState();
  // const [getConsoleOutputError, setGetConsoleOutputError] = useState();

  const currentOrg = useSelector((state) => state.user.currentOrg);

  useEffect(() => {
    requestPipelineRunConsoleOutput(currentOrg, pipelineInView, pipelineRunSelectedUuid)
      .then((response) => {
        if ('stdout' in response.data) setStdout(response.data.stdout);
        if ('stderr' in response.data) setStderr(response.data.stderr);
      })
      .catch(() => {
        // setGetConsoleOutputError(!err.response || err.response.data); // TODO: tell user output could not be gotten
      });
  });

  return (
    <StyledConsoleOutput>
      <header>
        <StyledH2 color="black">
          Run #
          {sequence}
        </StyledH2>
        <OverviewTabMenu displayTab={CONSOLE_OUTPUT_TAB} setDisplayTab={setDisplayTab} />
      </header>
      <section>
        <StyledH5 color="black">stdout:</StyledH5>
        {stdout}
        <br />
        <StyledH5 color="black">stderr:</StyledH5>
        {stderr}
      </section>
    </StyledConsoleOutput>

  );
};

ConsoleOutput.propTypes = {
  pipelineInView: PropTypes.string.isRequired,
  pipelineRunSelectedUuid: PropTypes.string.isRequired,
  sequence: PropTypes.number.isRequired,
  setDisplayTab: PropTypes.func.isRequired,
};

export default ConsoleOutput;
