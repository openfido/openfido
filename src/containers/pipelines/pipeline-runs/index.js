import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import { OVERVIEW_TAB, CONSOLE_OUTPUT_TAB } from 'config/pipeline-runs';
import { getPipelineRuns } from 'actions/pipelines';
import { StyledGrid } from 'styles/app';
import colors from 'styles/colors';
import StartRunPopup from './start-run-popup';
import OverviewTabMenu from './overview-tab-menu';
import ConsoleOutput from './console-output';
import Overview from './overview';
import AllRuns from './all-runs';
import FilesList from './files-list';

const PipelineRunsGrid = styled(StyledGrid)`
  align-items: start;
  grid-gap: 20px;
  grid-gap: 1.25rem;
  max-width: 1028px;
  overflow: hidden;
  padding: 12px 16px 20px 20px;
  padding: 0.75rem 1rem 1.25rem 1rem;
  section {
    background-color: ${colors.white};
    padding: 20px 28px 20px 16px;
    padding: 1.25rem 1.75rem 1.25rem 1rem;
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
  width: 318px;
  min-height: 429px;
`;

const ArtifactsSection = styled.section`
  grid-column: 3;
  grid-row: 2;
  width: 318px;
  min-height: 429px;
`;

const PipelineRuns = ({ pipelineInView }) => {
  const [showStartRunPopup, setStartRunPopup] = useState(false);
  const [selectedRun, setSelectedRun] = useState(null);
  const [displayTab, setDisplayTab] = useState(OVERVIEW_TAB);

  const pipelineRuns = useSelector((state) => state.pipelines.pipelineRuns);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const dispatch = useDispatch();

  const pipelineRunSelected = pipelineRuns && pipelineRuns.find((run) => run.uuid === selectedRun);

  useEffect(() => {
    dispatch(getPipelineRuns(currentOrg, pipelineInView));
  }, [currentOrg, pipelineInView, dispatch]);

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

  if (displayTab === CONSOLE_OUTPUT_TAB) {
    return (
      <ConsoleOutput
        pipelineInView={pipelineInView}
        sequence={pipelineRunSelected && pipelineRunSelected.sequence}
        setDisplayTab={setDisplayTab}
      />
    );
  }

  return (
    <>
      <PipelineRunsGrid gridTemplateColumns="1fr 1fr 1fr">
        <AllRunsSection>
          <AllRuns
            openStartRunPopup={openStartRunPopup}
            pipelineRuns={pipelineRuns}
            selectedRun={selectedRun}
            setSelectedRun={setSelectedRun}
          />
        </AllRunsSection>
        <OverviewSection>
          <OverviewTabMenu displayTab={displayTab} setDisplayTab={setDisplayTab} />
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
            pipelineRunSelected={pipelineRunSelected}
          />
        </InputFilesSection>
        <ArtifactsSection>
          <FilesList
            title="Artifacts"
            files={pipelineRunSelected && pipelineRunSelected.artifacts}
            pipelineRunSelected={pipelineRunSelected}
          />
        </ArtifactsSection>
      </PipelineRunsGrid>
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

PipelineRuns.propTypes = {
  pipelineInView: PropTypes.string.isRequired,
};

export default PipelineRuns;
