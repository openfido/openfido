import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useSelector } from 'react-redux';
import styled from 'styled-components';

import { requestPipelineRunConsoleOutput } from 'services';
import { CONSOLE_OUTPUT_TAB } from 'config/pipeline-runs';
import { pipelineStates } from 'config/pipeline-status';
import { StyledH2, StyledButton } from 'styles/app';
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
    white-space: pre-line;
  }
`;

const ConsoleOutputTypes = styled.div`
  padding-top: 16px;
  padding-top: 1rem;
`;

const ConsoleOutputContent = styled.div`
  padding: 20px 28px;
  padding: 1.25rem 1.75rem;
`;

const ConsoleOutput = ({
  pipelineInView, pipelineRunSelectedUuid, pipelineRunSelectedStatus, sequence, setDisplayTab,
}) => {
  const [stdout, setStdout] = useState();
  const [stderr, setStderr] = useState();
  const [outputType, setOutputType] = useState();
  // const [getConsoleOutputError, setGetConsoleOutputError] = useState();

  const currentOrg = useSelector((state) => state.user.currentOrg);

  useEffect(() => {
    requestPipelineRunConsoleOutput(currentOrg, pipelineInView, pipelineRunSelectedUuid)
      .then((response) => {
        if ('std_out' in response.data) setStdout(response.data.std_out);
        if ('std_err' in response.data) setStderr(response.data.std_err);
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
        <OverviewTabMenu
          displayTab={CONSOLE_OUTPUT_TAB}
          setDisplayTab={setDisplayTab}
          dataVisualizationReady={pipelineRunSelectedStatus === pipelineStates.COMPLETED}
        />
      </header>
      <section>
        <ConsoleOutputTypes>
          <StyledButton
            type="text"
            size="large"
            width={108}
            onClick={() => setOutputType('stdout')}
            textcolor={outputType === 'stdout' ? 'lightBlue' : 'black'}
          >
            stdout
          </StyledButton>
          <StyledButton
            type="text"
            size="large"
            width={108}
            onClick={() => setOutputType('stderr')}
            textcolor={outputType === 'stderr' ? 'lightBlue' : 'black'}
          >
            stderr
          </StyledButton>
        </ConsoleOutputTypes>
        <ConsoleOutputContent>
          {outputType === 'stdout' && stdout}
          {outputType === 'stderr' && stderr}
        </ConsoleOutputContent>
      </section>
    </StyledConsoleOutput>

  );
};

ConsoleOutput.propTypes = {
  pipelineInView: PropTypes.string.isRequired,
  pipelineRunSelectedUuid: PropTypes.string.isRequired,
  pipelineRunSelectedStatus: PropTypes.string.isRequired,
  sequence: PropTypes.number.isRequired,
  setDisplayTab: PropTypes.func.isRequired,
};

export default ConsoleOutput;
