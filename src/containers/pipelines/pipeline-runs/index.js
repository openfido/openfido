import React, { useState } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import {
  StyledGrid,
  StyledH3,
  StyledH4,
  StyledButton,
} from 'styles/app';
import colors from 'styles/colors';
import StartRunPopup from '../start-run-popup';

const PipelineRunsGrid = styled(StyledGrid)`
  justify-content: flex-start;
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
  h3 { 
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

const AllRunsSection = styled.section`
  grid-column: 1;
  grid-row: 1 / span 2;
  width: 318px;
  height: 686px;
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
  height: 398px;
`;

const ArtifactsSection = styled.section`
  grid-column: 3;
  grid-row: 2;
  width: 318px;
  height: 398px;
`;

export const PipelineRuns = ({ pipelineInView }) => {
  const [showStartRunPopup, setStartRunPopup] = useState(false);

  const openStartRunPopup = () => {
    setStartRunPopup(true);
  };

  const closeStartRunPopup = () => {
    setStartRunPopup(false);
  };

  return (
    <>
      <PipelineRunsGrid gridTemplateColumns="1fr 1fr 1fr">
        <AllRunsSection>
          <StyledH3 color="black">
            All Runs:
            <StyledButton type="text" onClick={openStartRunPopup}>
              + Start a run
            </StyledButton>
            <div />
          </StyledH3>
        </AllRunsSection>
        <OverviewSection><StyledH4 color="gray">Overview</StyledH4></OverviewSection>
        <InputFilesSection><StyledH4 color="gray">Input Files</StyledH4></InputFilesSection>
        <ArtifactsSection><StyledH4 color="gray">Artifacts</StyledH4></ArtifactsSection>
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
