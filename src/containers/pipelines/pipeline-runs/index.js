import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import PropTypes from 'prop-types';
import styled, { css } from 'styled-components';
import { Menu, Spin } from 'antd';
import moment from 'moment';

import {
  statusLegend,
  statusNameLegend,
  statusLongNameLegend,
  pipelineStates,
} from 'config/pipeline-status';
import LoadingFilled from 'icons/LoadingFilled';
import DownloadFilled from 'icons/DownloadFilled';
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
import { getPipelineRuns } from 'actions/pipelines';
import StartRunPopup from '../start-run-popup';
import OverviewTabMenu from './overview-tab-menu';
import ConsoleOutput from './console-output';

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

const FilesList = css`
  .anticon.anticon-download {
    margin-right: 4px;
    margin-right: 0.25rem;
    margin-left: -4px;
    margin-left: -0.25rem;
  }
  h3 {
    margin-left: 0.25rem;
    margin-top: 1rem;
    display: flex;
    justify-content: space-between;
  }
  ul {
    list-style-type: none;
    padding: 0;
    margin: 16px 0;
    margin: 1rem 0;
    li {
      display: flex;
      justify-content: space-between;
      font-size: 16px;
      font-size: 1rem;
      line-height: 19px;
      line-height: 1.195rem;
      padding: 12px 4px;
      padding: 0.75rem 0.25rem;
      color: ${colors.gray};
      a {
        color: ${colors.mediumBlue};
        font-weight: 500;
        &:hover {
          color: ${colors.lightBlue};
        }
      }
    }
  }
`;

const InputFilesSection = styled.section`
  grid-column: 2;
  grid-row: 2;
  width: 318px;
  min-height: 429px;
  ${FilesList}
`;

const ArtifactsSection = styled.section`
  grid-column: 3;
  grid-row: 2;
  width: 318px;
  min-height: 429px;
  ${FilesList}
  ul li > div {
    display: block;
    .anticon {
      right: -25px;
    }
  }
`;

const RunMenu = styled(Menu)`
  overflow: scroll;
  height: 617px;
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
    span {
      grid-column: 2 / span 2;
    }
    h4 {
      grid-column: 1 /span 2;
    }
    h5 {
      grid-column: 1;
    }
    mark {
      grid-column: 3;
    }
    h4, h5, span {
      letter-spacing: 0.05em;
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
  &.ant-menu-item-active {
    background-color: transparent;
  }
  &.ant-menu-item-selected {
    > div {
      border-radius: 6px;
      background-color: ${bgcolor in colors ? colors[bgcolor] : bgcolor};
      margin: 0;
      padding-left: 10px;
      padding-left: 0.625rem;
      padding-right: 10px;
      padding-right: 0.625rem;
      h4 {
        font-weight: bold;
      }
      h4, h5, span {
        color: ${colors.white};
      }
      mark {
        border: 1px solid ${colors.white};
      }
    }
    + li > div {
      border-top: 1px solid transparent;
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
  padding: 3px 0;
  text-align: center;
`;

const Overview = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  width: 294px;
  margin-top: 36px;
  margin-top: 2.25rem;
  h2 {
    margin-right: 16px;
    margin-right: 1rem;
  }
`;

const OverviewGrid = styled.div`
  display: grid;
  grid-gap: 12px;
  grid-gap: 0.75rem;
  span:not(.anticon) {
    display: block;
    margin-bottom: 0.25rem;
  }
  .anticon {
    left: 0;
    font-size: 20px;
  }
`;

const OverviewMeta = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  position: relative;
`;

const PipelineRuns = ({ pipelineInView }) => {
  const [showStartRunPopup, setStartRunPopup] = useState(false);
  const [selectedRun, setSelectedRun] = useState(null);
  const [displayTab, setDisplayTab] = useState('Overview');

  const pipelineRuns = useSelector((state) => state.pipelines.pipelineRuns);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const dispatch = useDispatch();

  const pipelineRunSelected = pipelineRuns && pipelineRuns.find((run) => run.uuid === selectedRun);

  const checkPipelineRunStatus = (run, statuses = []) => {
    let result = false;

    if (run && run.states && run.states.length) {
      statuses.forEach((status) => {
        if (run.states[0].state === status) {
          result = true;
        }
      });
    }

    return result;
  };

  const getPipelineRunStatus = (run) => run && run.states && run.states.length && run.states[0].state;

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

  if (displayTab === 'Console Output') {
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
          <StyledH2 color="black">
            All Runs:
            <StyledButton type="text" onClick={openStartRunPopup}>
              + Start a run
            </StyledButton>
            <div />
          </StyledH2>
          <RunMenu selectedKeys={[selectedRun]}>
            {pipelineRuns && pipelineRuns.map(({
              uuid: run_uuid, sequence, states, started_at,
            }) => {
              const status = states[0] && states[0].state;
              const momentStartedAt = moment.utc(started_at);

              return (
                <RunItem key={run_uuid} bgcolor={statusLegend[status]} onClick={() => setSelectedRun(run_uuid)}>
                  <div>
                    <StyledH4>
                      Run #
                      {sequence}
                    </StyledH4>
                    <StatusText>{statusNameLegend[status]}</StatusText>
                    <StyledH5>Started At:</StyledH5>
                    <StyledText size="middle" color="gray">{momentStartedAt.format('M/D/YY')}</StyledText>
                    <StyledH5>Duration:</StyledH5>
                    <StyledText size="middle" color="gray">{momentStartedAt.fromNow(true)}</StyledText>
                  </div>
                </RunItem>
              );
            })}
          </RunMenu>
        </AllRunsSection>
        <OverviewSection>
          <OverviewTabMenu displayTab={displayTab} setDisplayTab={setDisplayTab} />
          {pipelineRunSelected && (
            <Overview>
              <StyledH2 color="black">
                Run #
                {pipelineRunSelected.sequence}
              </StyledH2>
              <OverviewGrid>
                <div>
                  <StyledText size="middle" color="gray20" fontweight="bold">Started At:</StyledText>
                  <OverviewMeta>
                    <StyledText size="large" color="black" fontweight={500}>
                      {moment.utc(pipelineRunSelected.started_at).format('M/D/YY')}
                    </StyledText>
                    <StyledText size="large" color="black" fontweight={500}>
                      {moment.utc(pipelineRunSelected.started_at).format('h:m:sa')}
                    </StyledText>
                  </OverviewMeta>
                </div>
                <div>
                  <StyledText size="middle" color="gray20" fontweight="bold">Completed At:</StyledText>
                  <OverviewMeta>
                    {checkPipelineRunStatus(pipelineRunSelected, [pipelineStates.COMPLETED, pipelineStates.FAILED, pipelineStates.ABORTED]) ? (
                      <>
                        <StyledText size="large" color="black" fontweight={500}>
                          {moment.utc(pipelineRunSelected.updated_at).format('M/D/YY')}
                        </StyledText>
                        <StyledText size="large" color="black" fontweight={500}>
                          {moment.utc(pipelineRunSelected.updated_at).format('h:m:sa')}
                        </StyledText>
                      </>
                    ) : (
                      <>
                        <StyledText size="large" color="black" fontweight={500}>
                          {statusLongNameLegend[getPipelineRunStatus(pipelineRunSelected)]}
                        </StyledText>
                        {checkPipelineRunStatus(pipelineRunSelected, [pipelineStates.RUNNING]) && (
                        <Spin indicator={<LoadingFilled spin />} />
                        )}
                      </>
                    )}
                  </OverviewMeta>
                </div>
                <div />
                <div>
                  <StyledText size="middle" color="gray20" fontweight="bold">Duration</StyledText>
                  <StyledText size="large" color="black" fontweight={500}>
                    <OverviewMeta>
                      {checkPipelineRunStatus(pipelineRunSelected, [pipelineStates.COMPLETED, pipelineStates.FAILED, pipelineStates.ABORTED]) ? (
                        <>
                          <StyledText size="large" color="black" fontweight={500}>
                            {moment.utc(pipelineRunSelected.started_at).fromNow(true)}
                          </StyledText>
                        </>
                      ) : (
                        <>
                          <StyledText size="large" color="black" fontweight={500}>
                            {statusLongNameLegend[getPipelineRunStatus(pipelineRunSelected)]}
                          </StyledText>
                          {checkPipelineRunStatus(pipelineRunSelected, [pipelineStates.RUNNING]) && (
                            <Spin indicator={<LoadingFilled spin />} />
                          )}
                        </>
                      )}
                    </OverviewMeta>
                  </StyledText>
                </div>
              </OverviewGrid>
            </Overview>
          )}
        </OverviewSection>
        <InputFilesSection>
          <StyledH3 color="black">
            <span>Input Files</span>
            <span>Size</span>
          </StyledH3>
          <ul>
            {pipelineRunSelected && pipelineRunSelected && pipelineRunSelected.inputs.map(({
              uuid, name: file_name, url, size,
            }) => (
              <li key={uuid}>
                <a href={url}>
                  <DownloadFilled />
                  {file_name}
                </a>
                <span>{size}</span>
              </li>
            ))}
          </ul>
        </InputFilesSection>
        <ArtifactsSection>
          <StyledH3 color="black">
            <span>Artifacts</span>
            <span>Size</span>
          </StyledH3>
          {pipelineRunSelected && pipelineRunSelected.artifacts && pipelineRunSelected.artifacts.length ? (
            <ul>
              {pipelineRunSelected.artifacts.map(({
                uuid, name: file_name, url, size,
              }) => (
                <li key={uuid}>
                  <a href={url}>
                    <DownloadFilled />
                    {file_name}
                  </a>
                  <span>{size}</span>
                </li>
              ))}
            </ul>
          ) : (
            <ul>
              <li>
                <OverviewMeta>
                  <StyledText size="large" color="black" fontweight={500}>
                    {statusLongNameLegend[getPipelineRunStatus(pipelineRunSelected)]}
                  </StyledText>
                  {checkPipelineRunStatus(pipelineRunSelected, [pipelineStates.RUNNING]) && (
                  <Spin indicator={<LoadingFilled spin />} />
                  )}
                </OverviewMeta>
              </li>
            </ul>
          )}
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
