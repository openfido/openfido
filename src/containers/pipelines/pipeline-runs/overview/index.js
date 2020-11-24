import React from 'react';
import PropTypes from 'prop-types';
import { Spin } from 'antd';

import { StyledH2, StyledText } from 'styles/app';
import { PIPELINE_STATES, STATUS_LONG_NAME_LEGEND } from 'config/pipelines';
import LoadingFilled from 'icons/LoadingFilled';
import styled from 'styled-components';

const StyledOverview = styled.div`
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

const Overview = ({ pipelineRunSelected: run }) => {
  const {
    status: runStatus, startedAt, completedAt, duration,
  } = run;

  const checkPipelineRunStatus = (statuses = []) => {
    let result = false;

    statuses.forEach((status) => {
      if (runStatus === status) {
        result = true;
      }
    });

    return result;
  };

  return (
    <StyledOverview>
      <StyledH2 color="black">
        Run #
        {run.sequence}
      </StyledH2>
      <OverviewGrid>
        <div>
          <StyledText size="middle" color="gray20" fontweight="bold">Started At:</StyledText>
          <OverviewMeta>
            {startedAt ? (
              <>
                <StyledText size="large" color="black" fontweight={500}>
                  {startedAt.format('M/D/YY')}
                </StyledText>
                <StyledText size="large" color="black" fontweight={500}>
                  {startedAt.format('h:mm:ssa')}
                </StyledText>
              </>
            ) : (
              <StyledText size="large" color="black" fontweight={500}>
                {STATUS_LONG_NAME_LEGEND[runStatus]}
              </StyledText>
            )}
          </OverviewMeta>
        </div>
        <div>
          <StyledText size="middle" color="gray20" fontweight="bold">Completed At:</StyledText>
          <OverviewMeta>
            {checkPipelineRunStatus([PIPELINE_STATES.COMPLETED, PIPELINE_STATES.FAILED, PIPELINE_STATES.CANCELED]) ? (
              <>
                <StyledText size="large" color="black" fontweight={500}>
                  {completedAt && completedAt.format('M/D/YY')}
                </StyledText>
                <StyledText size="large" color="black" fontweight={500}>
                  {completedAt && completedAt.format('h:mm:ssa')}
                </StyledText>
              </>
            ) : (
              <>
                <StyledText size="large" color="black" fontweight={500}>
                  {STATUS_LONG_NAME_LEGEND[runStatus]}
                </StyledText>
                {runStatus === PIPELINE_STATES.RUNNING && (
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
              {checkPipelineRunStatus([PIPELINE_STATES.COMPLETED, PIPELINE_STATES.FAILED, PIPELINE_STATES.CANCELED]) ? (
                <>
                  <StyledText size="large" color="black" fontweight={500}>
                    {duration}
                  </StyledText>
                </>
              ) : (
                <>
                  <StyledText size="large" color="black" fontweight={500}>
                    {STATUS_LONG_NAME_LEGEND[runStatus]}
                  </StyledText>
                  {runStatus === PIPELINE_STATES.RUNNING && (
                    <Spin indicator={<LoadingFilled spin />} />
                  )}
                </>
              )}
            </OverviewMeta>
          </StyledText>
        </div>
      </OverviewGrid>
    </StyledOverview>
  );
};

Overview.propTypes = {
  pipelineRunSelected: PropTypes.shape({
    sequence: PropTypes.number.isRequired,
    states: PropTypes.arrayOf(PropTypes.shape({
      state: PropTypes.string.isRequired,
    })),
  }).isRequired,
};

export default Overview;
