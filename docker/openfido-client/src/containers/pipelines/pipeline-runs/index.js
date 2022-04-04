import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import styled from 'styled-components';
// import axios from "axios";

import {
  PIPELINE_STATES,
  POLL_PIPELINE_RUN_INTERVAL,
  STATUS_LONG_NAME_LEGEND,
} from 'config/pipelines';
import {
  getPipelineRuns,
  getPipelineRun,
  getPipelines,
  // getPipelineConfigData,
} from 'actions/pipelines';
import { StyledGrid, StyledText, StyledTitle } from 'styles/app';
import colors from 'styles/colors';
import StartRunPopup from './start-run-popup';
import OverviewTabMenu from './overview-tab-menu';
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
  position: relative;
  .ant-spin .anticon {
    top: calc(50% - 8px);
    left: calc(50% - 8px);
  }
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
  .anticon {
    width: 16px;
    height: 16px;
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

  const pipelines = useSelector((state) => state.pipelines.pipelines);
  let configUrl = null;
  let piplineUrl = null;
  let pipelineBranch = null;
  if (pipelines !== null) {
    pipelines.forEach((pipeline) => {
      if (pipeline.uuid === pipelineInView) {
        // configUrl generates the API url for github to retrieve the manifest.json file
        configUrl = pipeline.repository_ssh_url.replace('.git', '').replace('github.com/', 'api.github.com/repos/');
        piplineUrl = pipeline.repository_ssh_url;
        pipelineBranch = pipeline.repository_branch;
      }
    });
  }
  const pipelineRuns = useSelector((state) => state.pipelines.pipelineRuns[pipelineInView]);
  const getPipelineRunsInProgress = useSelector((state) => state.pipelines.messages.getPipelineRunsInProgress);
  const currentPipelineRun = useSelector((state) => state.pipelines.currentPipelineRunUuids[pipelineInView]);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const dispatch = useDispatch();

  const pipelineRunSelected = useSelector((state) => state.pipelines.currentPipelineRuns[pipelineInView]);
  const getPipelineRunInProgress = useSelector((state) => state.pipelines.messages.getPipelineRunInProgress);
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
    if (!getPipelineRunsInProgress && !pipelineRuns) {
      dispatch(getPipelineRuns(currentOrg, pipelineInView));
    }
  }, [currentOrg, pipelineInView, dispatch, getPipelineRunsInProgress, pipelineRuns]);

  useEffect(() => {
    const interval = currentPipelineRun && !getPipelineRunInProgress && setInterval(() => {
      dispatch(getPipelineRun(currentOrg, pipelineInView, currentPipelineRun));
    }, POLL_PIPELINE_RUN_INTERVAL);
    return () => clearInterval(interval);
  }, [currentOrg, pipelineInView, currentPipelineRun, getPipelineRunInProgress, dispatch]);

  useEffect(() => {
    if (!getPipelineRunInProgress && pipelineRuns && pipelineRuns.length && !currentPipelineRun) {
      dispatch(getPipelineRun(currentOrg, pipelineInView, pipelineRuns[0].uuid));
    }
  }, [pipelineRuns, currentPipelineRun, currentOrg, pipelineInView, dispatch, getPipelineRunInProgress]);

  const onSelectPipelineRun = (pipelineRunSelectedUuid) => {
    if (!getPipelineRunInProgress) {
      dispatch(getPipelineRun(currentOrg, pipelineInView, pipelineRunSelectedUuid));
    }
  };

  const openStartRunPopup = () => {
    setStartRunPopup(true);
  };

  const closeStartRunPopup = (runStarted) => {
    setStartRunPopup(false);
    if (runStarted) dispatch(getPipelineRuns(currentOrg, pipelineInView));
  };

  const handleDeletePipelineRunSuccess = () => {
    dispatch(getPipelineRuns(currentOrg, pipelineInView));
  };

  return (
    <React.Fragment key={pipelineInView}>
      <StyledTitle>
        <div>
          <h1>
            Pipeline Runs:
            {' '}
            <StyledText color="blue">{pipelineItemInView && pipelineItemInView.name}</StyledText>
          </h1>
        </div>
      </StyledTitle>
      <PipelineRunsGrid gridTemplateColumns="1fr 1fr 1fr">
        <AllRunsSection>
          <RunsList
            openStartRunPopup={openStartRunPopup}
            pipelineRuns={pipelineRuns}
            currentPipelineRun={currentPipelineRun}
            onSelectPipelineRun={onSelectPipelineRun}
            currentPipeline={pipelineInView}
            handleSuccess={handleDeletePipelineRunSuccess}
          />
        </AllRunsSection>
        <OverviewSection>
          <OverviewTabMenu
            dataVisualizationReady={pipelineRunSelected && pipelineRunSelected.status === PIPELINE_STATES.COMPLETED}
            consoleOutputReady={!!pipelineRunSelected}
            pipelineInView={pipelineInView}
            pipelineRunSelectedUuid={pipelineRunSelected && pipelineRunSelected.uuid}
          />
          {!!pipelineRunSelected && (
            <Overview
              pipelineRunSelected={pipelineRunSelected}
            />
          )}
        </OverviewSection>
        <InputFilesSection>
          <FilesList
            title="Input Files"
            files={pipelineRunSelected && pipelineRunSelected.inputs}
            emptyText={!!pipelineRunSelected && !pipelineRunSelected.length ? 'No Input Files' : null}
          />
        </InputFilesSection>
        <ArtifactsSection>
          <FilesList
            title="Artifacts"
            files={pipelineRunSelected && pipelineRunSelected.artifacts}
            pipelineRunStatus={pipelineRunStatus}
            emptyText={STATUS_LONG_NAME_LEGEND[pipelineRunStatus]}
          />
        </ArtifactsSection>
      </PipelineRunsGrid>
      {showStartRunPopup && (
        <StartRunPopup
          handleOk={closeStartRunPopup}
          handleCancel={closeStartRunPopup}
          pipeline_uuid={pipelineInView}
          configUrl={configUrl}
          piplineUrl={piplineUrl}
          pipelineBranch={pipelineBranch}
        />
      )}
    </React.Fragment>
  );
};

export default PipelineRuns;
