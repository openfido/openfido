import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';

import { requestPipelineRunConsoleOutput } from 'services';
import { STDOUT, STDERR } from 'config/pipeline-runs';
import { getPipelineRun, getPipelines } from 'actions/pipelines';
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

const ConsoleOutput = () => {
  const { pipeline_uuid: pipelineInView, pipeline_run_uuid: pipelineRunSelectedUuid } = useParams();

  const [stdout, setStdout] = useState();
  const [stderr, setStderr] = useState();
  const [outputType, setOutputType] = useState(STDOUT);
  const [getConsoleOutputError, setGetConsoleOutputError] = useState(null);

  const currentOrg = useSelector((state) => state.user.currentOrg);
  const pipelines = useSelector((state) => state.pipelines.pipelines);
  const currentPipelineRun = useSelector((state) => state.pipelines.currentPipelineRun);
  const currentPipelineRunUuid = useSelector((state) => state.pipelines.currentPipelineRunUuid);
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

  useEffect(() => {
    requestPipelineRunConsoleOutput(currentOrg, pipelineInView, pipelineRunSelectedUuid)
      .then((response) => {
        if (STDOUT in response.data) setStdout(response.data[STDOUT]);
        if (STDERR in response.data) setStderr(response.data[STDERR]);
        setGetConsoleOutputError(null);
      })
      .catch((err) => {
        setGetConsoleOutputError(!err.response || err.response.data);
      });
  }, [currentOrg, pipelineInView, pipelineRunSelectedUuid]);

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
            dataVisualizationReady
            consoleOutputReady
            pipelineInView={pipelineInView}
            pipelineRunSelectedUuid={pipelineRunSelectedUuid}
          />
        </header>
        <section>
          <ConsoleOutputTypes>
            <StyledButton
              type="text"
              size="large"
              width={108}
              onClick={() => setOutputType(STDOUT)}
              textcolor={outputType === STDOUT ? 'lightBlue' : 'gray'}
            >
              stdout
            </StyledButton>
            <StyledButton
              type="text"
              size="large"
              width={108}
              onClick={() => setOutputType(STDERR)}
              textcolor={outputType === STDERR ? 'lightBlue' : 'gray'}
            >
              stderr
            </StyledButton>
          </ConsoleOutputTypes>
          <ConsoleOutputContent>
            {getConsoleOutputError && 'message' in getConsoleOutputError && getConsoleOutputError.message}
            {outputType === STDOUT && stdout}
            {outputType === STDERR && stderr}
          </ConsoleOutputContent>
        </section>
      </StyledConsoleOutput>
    </>
  );
};

export default ConsoleOutput;
