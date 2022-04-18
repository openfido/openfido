import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Spin } from 'antd';
import styled from 'styled-components';

import {
  STDOUT,
  STDERR,
  PIPELINE_STATES,
  POLL_CONSOLE_OUTPUT_INTERVAL,
} from 'config/pipelines';
import {
  getPipelines,
  getPipelineRun,
  getPipelineRunConsoleOutput,
} from 'actions/pipelines';
import LoadingFilled from 'icons/LoadingFilled';
import {
  StyledH2, StyledButton, StyledTitle, StyledText,
} from 'styles/app';
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
    text-align: center;
    .ant-spin .anticon {
      position: static;
      margin-top: 2.5rem;
    }
  }
`;

const ConsoleOutputTypes = styled.div`
  display: flex;
  flex-direction: row;
  padding-top: 16px;
  padding-top: 1rem;
  text-align: left;
`;

const ConsoleOutputContent = styled.div`
  padding: 20px 28px;
  padding: 1.25rem 1.75rem;
  text-align: left;
`;

const ButtonContainer = styled.div`
display: flex;
box-shadow: 10px 5px 5px black;
border: 1px solid;
margin: 15px;
max-width: 40%;
min-width: 40%;
text-align: left;
justify-content: center;
align-items: center;
`;

const ConsoleOutput = () => {
  const { pipeline_uuid: pipelineInView, pipeline_run_uuid: pipelineRunSelectedUuid } = useParams();

  const [outputType, setOutputType] = useState(STDOUT);

  const currentOrg = useSelector((state) => state.user.currentOrg);
  const pipelines = useSelector((state) => state.pipelines.pipelines);
  const currentPipelineRun = useSelector((state) => state.pipelines.currentPipelineRuns[pipelineInView]);
  const currentPipelineRunUuid = useSelector((state) => state.pipelines.currentPipelineRunUuids[pipelineInView]);
  const consoleOutput = useSelector((state) => state.pipelines.consoleOutput);
  const getConsoleOutputInProgress = useSelector((state) => state.pipelines.messages.getPipelineRunConsoleOutputInProgress);
  const getConsoleOutputError = useSelector((state) => state.pipelines.messages.getPipelineRunConsoleOutputError);
  const dispatch = useDispatch();

  const pipelineItemInView = pipelines && pipelines.find((pipelineItem) => pipelineItem.uuid === pipelineInView);

  useEffect(() => {
    if (!pipelines && !pipelineItemInView) {
      dispatch(getPipelines(currentOrg));
    }
  }, [currentOrg, dispatch, pipelines, pipelineItemInView]);

  useEffect(() => {
    if (currentPipelineRunUuid !== pipelineRunSelectedUuid || !currentPipelineRun) {
      dispatch(getPipelineRun(currentOrg, pipelineInView, pipelineRunSelectedUuid));
    }
  }, [currentOrg, pipelineInView, pipelineRunSelectedUuid, currentPipelineRunUuid, currentPipelineRun, dispatch]);

  // Refreshes console output after the time set in interval
  useEffect(() => {
    const interval = pipelineRunSelectedUuid && !getConsoleOutputInProgress && setInterval(() => {
      dispatch(getPipelineRunConsoleOutput(currentOrg, pipelineInView, pipelineRunSelectedUuid, true));
    }, POLL_CONSOLE_OUTPUT_INTERVAL);
    return () => clearInterval(interval);
  }, [currentOrg, pipelineInView, pipelineRunSelectedUuid, getConsoleOutputInProgress, dispatch]);

  // run once version of above useEffect to quickly refresh console data when switching between runs
  useEffect(() => {
    const updateOnce = pipelineRunSelectedUuid && !getConsoleOutputInProgress && setTimeout(() => {
      dispatch(getPipelineRunConsoleOutput(currentOrg, pipelineInView, pipelineRunSelectedUuid, true));
    }, 500);
    return () => clearTimeout(updateOnce);
  }, [currentOrg, pipelineInView, pipelineRunSelectedUuid, getConsoleOutputInProgress, dispatch]);

  useEffect(() => {
    if (!getConsoleOutputInProgress && consoleOutput && !consoleOutput[outputType]) {
      dispatch(getPipelineRunConsoleOutput(currentOrg, pipelineInView, pipelineRunSelectedUuid, true));
    }
  }, [
    consoleOutput, outputType, currentOrg, pipelineInView, pipelineRunSelectedUuid, getConsoleOutputInProgress, dispatch,
  ]);

  return (
    <>
      <StyledTitle>
        <div>
          <h1>
            Pipeline Runs:
            {' '}
            <StyledText color="blue">{pipelineItemInView && pipelineItemInView.name}</StyledText>
          </h1>
        </div>
      </StyledTitle>
      <StyledConsoleOutput>
        <header>
          <StyledH2 color="black">
            Run #
            {currentPipelineRun && currentPipelineRun.sequence}
          </StyledH2>
          <OverviewTabMenu
            dataVisualizationReady={currentPipelineRun && currentPipelineRun.status === PIPELINE_STATES.COMPLETED}
            consoleOutputReady
            pipelineInView={pipelineInView}
            pipelineRunSelectedUuid={pipelineRunSelectedUuid}
          />
        </header>
        <section>
          <ConsoleOutputTypes>
            <ButtonContainer style={{ borderColor: outputType === STDOUT ? 'lightBlue' : 'black' }}>
              <StyledButton
                type="text"
                size="large"
                width={108}
                onClick={() => setOutputType(STDOUT)}
                textcolor={outputType === STDOUT ? 'lightBlue' : 'gray'}
              >
                STANDARD OUTPUT
                <br />
                (stdout)
              </StyledButton>
            </ButtonContainer>
            <ButtonContainer style={{ borderColor: outputType === STDERR ? 'lightBlue' : 'black' }}>
              <StyledButton
                type="text"
                size="large"
                width={108}
                onClick={() => setOutputType(STDERR)}
                textcolor={outputType === STDERR ? 'lightBlue' : 'gray'}
              >
                STANDARD ERROR
                <br />
                (stderr)
              </StyledButton>
            </ButtonContainer>
          </ConsoleOutputTypes>
          {(getConsoleOutputError || (consoleOutput && !consoleOutput[outputType])) && (
            <Spin indicator={<LoadingFilled spin />} />
          )}
          <ConsoleOutputContent>
            {getConsoleOutputError && getConsoleOutputError.message}
            {consoleOutput && consoleOutput[outputType]}
          </ConsoleOutputContent>
        </section>
      </StyledConsoleOutput>
    </>
  );
};

export default ConsoleOutput;
