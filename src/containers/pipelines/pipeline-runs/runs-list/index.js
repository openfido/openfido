import React from 'react';
import PropTypes from 'prop-types';
import { useSelector } from 'react-redux';
import styled from 'styled-components';
import { Menu, Spin } from 'antd';

import {
  STATUS_LEGEND,
  STATUS_NAME_LEGEND,
} from 'config/pipelines';
import LoadingFilled from 'icons/LoadingFilled';
import {
  StyledButton,
  StyledH2,
  StyledH4,
  StyledH5,
  StyledText,
} from 'styles/app';
import colors from 'styles/colors';

const RunMenu = styled(Menu)`
  overflow-y: scroll;
  height: 617px;
  margin-right: -28px;
  &.ant-menu-vertical {
    border-right: 0;
    > .ant-menu-item {
      height: auto;
      line-height: inherit;
      padding: 0;
      overflow: visible;
    }
    .ant-menu-item-selected, .ant-menu-item-active {
      background-color: transparent;
    }
  } 
`;

const RunItem = styled(Menu.Item)`
  position: relative;
  margin-right: 19px;
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

const Caret = styled.div`
  width: 0; 
  height: 0; 
  border-top: 14px solid transparent;
  border-bottom: 14px solid transparent;
  border-left: 14px solid ${({ bgcolor }) => (bgcolor in colors ? colors[bgcolor] : '')};
  position: absolute;
  right: -8px;
`;

const RunsList = ({
  openStartRunPopup, pipelineRuns, currentPipelineRun, onSelectPipelineRun,
}) => {
  const getPipelineRunsInProgress = useSelector((state) => state.pipelines.messages.getPipelineRunsInProgress);

  return (
    <>
      <StyledH2 color="black">
        All Runs:
        <StyledButton type="text" onClick={openStartRunPopup}>
          + Start a run
        </StyledButton>
        <div />
      </StyledH2>
      {getPipelineRunsInProgress && (
        <Spin indicator={<LoadingFilled spin />} />
      )}
      <RunMenu selectedKeys={[currentPipelineRun]}>
        {!getPipelineRunsInProgress && pipelineRuns && pipelineRuns.map(({
          uuid: run_uuid, sequence, status, startedAt, duration,
        }) => (
          <RunItem key={run_uuid} bgcolor={STATUS_LEGEND[status]} onClick={() => onSelectPipelineRun(run_uuid)}>
            <div>
              <StyledH4>
                Run #
                {sequence}
              </StyledH4>
              <StatusText>{STATUS_NAME_LEGEND[status]}</StatusText>
              <StyledH5>Started At:</StyledH5>
              {startedAt && (
                <StyledText size="middle" color="gray">
                  {startedAt.format('M/D/YY')}
                </StyledText>
              )}
              <StyledH5>Duration:</StyledH5>
              {duration && (
                <StyledText size="middle" color="gray">
                  {duration}
                </StyledText>
              )}
              {currentPipelineRun === run_uuid && <Caret bgcolor={STATUS_LEGEND[status]} />}
            </div>
          </RunItem>
        ))}
      </RunMenu>
    </>
  );
};

RunsList.propTypes = {
  openStartRunPopup: PropTypes.func.isRequired,
  pipelineRuns: PropTypes.arrayOf(PropTypes.shape({

  })),
  currentPipelineRun: PropTypes.string,
  onSelectPipelineRun: PropTypes.func.isRequired,
};

RunsList.defaultProps = {
  pipelineRuns: [],
  currentPipelineRun: null,
};

export default RunsList;
