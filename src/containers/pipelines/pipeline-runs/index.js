import React, { useState } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { Menu } from 'antd';

import {
  StyledGrid,
  StyledH2,
  StyledH3,
  StyledH4,
  StyledH5,
  StyledText,
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

const RunMenu = styled(Menu)`
  &.ant-menu-vertical {
    border-right: 0;
   > .ant-menu-item {
    height: auto;
    line-height: inherit;
    padding: 0;
    }
  }
  &.ant-menu:not(.ant-menu-horizontal) .ant-menu-item-selected {
    background-color: transparent;
  }
`;

const RunItem = styled(Menu.Item)`
  > div {
    display: grid;
    align-items: center;
    grid-template-columns: auto 1fr 0.5fr;
    grid-column-gap: 16px;
    grid-column-gap: 1rem;
    grid-row-gap: 4px;
    grid-row-gap: 0.25rem;
    margin: 0 10px;
    padding: 20px 0;
    padding: 1.25rem 0;
    h4, h5 {
      grid-column: 1;
    }
    > mark {
      grid-column: 3;
    }
  }
  ${({ bgcolor }) => (`
  ${bgcolor ? (`
  > div > mark {
    background-color: ${bgcolor in colors ? colors[bgcolor] : bgcolor};
    color: ${colors.white};
    border: 1px solid transparent;
    background-clip: padding-box;
  }
  &.ant-menu-item-selected {
    > div {
      border-radius: 6px;
      background-color: ${bgcolor in colors ? colors[bgcolor] : bgcolor};
      margin: 0;
      padding: 20px 10px;
      padding: 1.25rem 0.625rem;
      h4, h5, span {
        color: ${colors.white};
      }
      mark {
        border: 1px solid ${colors.white};
      }
    }
    + li > div {
      border-top: 0;
    }
  }
  &:not(:first-child) {
    > div {
      border-top: 1px solid ${colors.gray20};
    }
  }
  `) : ''}
  `)}
`;

const StatusText = styled.mark`
  border-radius: 2px;
  width: 68px;
  font-size: 12px;
  line-height: 14px;
  text-align: center;
`;

const PipelineRuns = ({ pipelineInView }) => {
  const [showStartRunPopup, setStartRunPopup] = useState(false);
  const [selectedRun, setSelectedRun] = useState('run6');

  const openStartRunPopup = () => {
    setStartRunPopup(true);
  };

  const closeStartRunPopup = () => {
    setStartRunPopup(false);
  };

  const statusLegend = {
    NOT_STARTED: 'skyBlue',
    RUNNING: 'lightBlue',
    COMPLETED: 'green',
    FAILED: 'pink',
  };

  return (
    <>
      <PipelineRunsGrid gridTemplateColumns="1fr 1fr 1fr">
        <AllRunsSection>
          <StyledH2 color="black">
            All Runs:
            <StyledButton type="text" onClick={openStartRunPopup}>
              + Start a run
            </StyledButton>
            <div />
          </StyledH2>
          <RunMenu selectedKeys={[selectedRun]}>
            <RunItem key="run6" bgcolor={statusLegend.RUNNING} onClick={() => setSelectedRun('run6')}>
              <div>
                <StyledH4>Run #6</StyledH4>
                <StatusText>Canceled</StatusText>
                <StyledH5>Started At: </StyledH5>
                <StyledText size="middle" color="gray">8/6/20</StyledText>
                <StyledH5>Duration:</StyledH5>
                <StyledText size="middle" color="gray">26 minutes</StyledText>
              </div>
            </RunItem>
            <RunItem key="run5" bgcolor={statusLegend.NOT_STARTED} onClick={() => setSelectedRun('run5')}>
              <div>
                <StyledH4>Run #5</StyledH4>
                <StatusText>In Queue</StatusText>
                <StyledH5>Started At: </StyledH5>
                <StyledText size="middle" color="gray">8/6/20</StyledText>
                <StyledH5>Duration:</StyledH5>
                <StyledText size="middle" color="gray">26 minutes</StyledText>
              </div>
            </RunItem>
            <RunItem key="run4" bgcolor={statusLegend.COMPLETED} onClick={() => setSelectedRun('run4')}>
              <div>
                <StyledH4>Run #4</StyledH4>
                <StatusText>Completed</StatusText>
                <StyledH5>Started At: </StyledH5>
                <StyledText size="middle" color="gray">8/6/20</StyledText>
                <StyledH5>Duration:</StyledH5>
                <StyledText size="middle" color="gray">26 minutes</StyledText>
              </div>
            </RunItem>
            <RunItem key="run3" bgcolor={statusLegend.FAILED} onClick={() => setSelectedRun('run3')}>
              <div>
                <StyledH4>Run #4</StyledH4>
                <StatusText>Failed</StatusText>
                <StyledH5>Started At: </StyledH5>
                <StyledText size="middle" color="gray">8/6/20</StyledText>
                <StyledH5>Duration:</StyledH5>
                <StyledText size="middle" color="gray">26 minutes</StyledText>
              </div>
            </RunItem>
          </RunMenu>
        </AllRunsSection>
        <OverviewSection>
          <StyledH4 color="gray">Overview</StyledH4>
        </OverviewSection>
        <InputFilesSection><StyledH3 color="black">Input Files</StyledH3></InputFilesSection>
        <ArtifactsSection><StyledH3 color="black">Artifacts</StyledH3></ArtifactsSection>
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
