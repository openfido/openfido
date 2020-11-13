import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import styled from 'styled-components';

import {
  OVERVIEW_TAB,
  DATA_VISUALIZATION_TAB,
  CONSOLE_OUTPUT_TAB,
} from 'config/pipeline-runs';
import { pipelineStates } from 'config/pipeline-status';
import { getPipelineRuns, getPipelines } from 'actions/pipelines';
import { StyledGrid, StyledText, StyledTitle } from 'styles/app';
import colors from 'styles/colors';
import StartRunPopup from './start-run-popup';
import OverviewTabMenu from './overview-tab-menu';
import ConsoleOutput from './console-output';
import DataVisualization from './data-visualization';
import Overview from './overview';
import RunsList from './runs-list';
import FilesList from './files-list';

const PipelineRunsGrid = styled(StyledGrid)`
  align-items: start;
  grid-gap: 20px;
  grid-gap: 1.25rem;
  max-width: 1028px;
  overflow: hidden;
  padding: 12px 2px 20px 20px;
  padding: 0.75rem 0.125rem 1.25rem 1rem;
  section {
    background-color: ${colors.white};
    padding: 20px 28px 20px 16px;
    padding: 1.25rem 1.75rem 1.25rem 1rem;
    border-radius: 5px;
  }
`;

const AllRunsSection = styled.section`
  grid-column: 1;
  grid-row: 1 / span 2;
  width: 318px;
  height: 718px;
  h2 { 
     width: 100%;
     padding-bottom: 3px;
     padding-left: 16px;
     padding-left: 1rem;
     overflow: hidden;
     .ant-btn {
       float: right;
       padding: 4px;
       font-weight: bold;
     }
     > div {
        width: calc(100% + 16px);
        height: 10px;
        height: 0.625rem;
        position: relative;
        left: -1rem;
        box-shadow: 0px 1px 3px -1px rgba(0, 0, 0, 0.1);
      }
  }
`;

const OverviewSection = styled.section`
  grid-column: 2 / span 2;
  grid-row: 1;
  width: 656px;
  height: 268px;
`;

const InputFilesSection = styled.section`
  grid-column: 2;
  grid-row: 2;
  width: 314px;
  min-height: 429px;
  padding: 0;
`;

const ArtifactsSection = styled.section`
  grid-column: 3;
  grid-row: 2;
  width: 314px;
  min-height: 429px;
`;

const PipelineRuns = () => {
  const { pipeline_uuid: pipelineInView } = useParams();

  const [showStartRunPopup, setStartRunPopup] = useState(false);
  const [selectedRun, setSelectedRun] = useState(null);
  const [displayTab, setDisplayTab] = useState(OVERVIEW_TAB);

  const pipelines = useSelector((state) => state.pipelines.pipelines);
  const pipelineRuns = useSelector((state) => state.pipelines.pipelineRuns[pipelineInView]);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const dispatch = useDispatch();

  const pipelineRunSelected = pipelineRuns && pipelineRuns.find((run) => run.uuid === selectedRun);
  const pipelineItemInView = pipelines && pipelines.find((pipelineItem) => pipelineItem.uuid === pipelineInView);
  const pipelineRunStatus = (
    pipelineRunSelected
      && pipelineRunSelected.states
      && pipelineRunSelected.states.length
      && pipelineRunSelected.states[pipelineRunSelected.states.length - 1].state
  );

  useEffect(() => {
    if (!pipelines) {
      dispatch(getPipelines(currentOrg));
    }
  }, [currentOrg, dispatch, pipelines]);

  useEffect(() => {
    dispatch(getPipelineRuns(currentOrg, pipelineInView));
  }, [currentOrg, pipelineInView, dispatch, showStartRunPopup]);

  useEffect(() => {
    if (pipelineRuns && pipelineRuns.length) {
      setSelectedRun(pipelineRuns[0].uuid);
    }
  }, [pipelineRuns]);

  const openStartRunPopup = () => {
    setStartRunPopup(true);
  };

  const closeStartRunPopup = () => {
    setStartRunPopup(false);
  };

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
      {displayTab === OVERVIEW_TAB && (
        <PipelineRunsGrid gridTemplateColumns="1fr 1fr 1fr">
          <AllRunsSection>
            <RunsList
              openStartRunPopup={openStartRunPopup}
              pipelineRuns={pipelineRuns}
              selectedRun={selectedRun}
              setSelectedRun={setSelectedRun}
            />
          </AllRunsSection>
          <OverviewSection>
            <OverviewTabMenu
              displayTab={displayTab}
              setDisplayTab={setDisplayTab}
              dataVisualizationReady={pipelineRunSelected && pipelineRunSelected.status === pipelineStates.COMPLETED}
              consoleOutputReady={!!pipelineRunSelected}
            />
            {pipelineRunSelected && (
              <Overview
                pipelineRunSelected={pipelineRunSelected}
              />
            )}
          </OverviewSection>
          <InputFilesSection>
            <FilesList
              title="Input Files"
              files={pipelineRunSelected && pipelineRunSelected.inputs}
              pipelineRunStatus={pipelineRunStatus}
            />
          </InputFilesSection>
          <ArtifactsSection>
            <FilesList
              title="Artifacts"
              files={pipelineRunSelected && pipelineRunSelected.artifacts}
              pipelineRunStatus={pipelineRunStatus}
            />
          </ArtifactsSection>
        </PipelineRunsGrid>
      )}
      {displayTab === CONSOLE_OUTPUT_TAB && (
        <ConsoleOutput
          pipelineInView={pipelineInView}
          pipelineRunSelectedUuid={pipelineRunSelected && pipelineRunSelected.uuid}
          pipelineRunSelectedStatus={pipelineRunSelected && pipelineRunSelected.status}
          sequence={pipelineRunSelected && pipelineRunSelected.sequence}
          setDisplayTab={setDisplayTab}
        />
      )}
      {displayTab === DATA_VISUALIZATION_TAB && (
        <DataVisualization
          pipelineInView={pipelineInView}
          pipelineRunSelected={pipelineRunSelected}
          sequence={pipelineRunSelected && pipelineRunSelected.sequence}
          setDisplayTab={setDisplayTab}
        />
      )}
      {showStartRunPopup && (
        <StartRunPopup
          handleOk={closeStartRunPopup}
          handleCancel={closeStartRunPopup}
          pipeline_uuid={pipelineInView}
        />
      )}
    </>
  );
};

export default PipelineRuns;
