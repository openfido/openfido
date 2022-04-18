import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import {
  STATUS_LEGEND,
  STATUS_NAME_LEGEND,
  STATUS_PHRASE_LEGEND,
} from 'config/pipelines';
import EditOutlined from 'icons/EditOutlined';
import {
  StyledGrid,
  StyledButton,
  StyledText,
} from 'styles/app';
import moment from 'moment';
import colors from 'styles/colors';

const PipelineItemGrid = styled(StyledGrid)`
  text-align: left;
  box-shadow: 10px 5px 5px black;
  border: 1px solid;
  .ant-btn {
    height: 32px;
    height: 2rem;
  }
`;

const StatusLegend = styled.div`
  height: 16px;
  height: 1rem;
  width: 16px;
  width: 1rem;
  margin: 0 16px;
  margin: 1rem;
  ${({ color }) => (`
  background-color: ${color in colors ? colors[color] : 'transparent'};
  `)}
`;

const ViewRunsColumn = styled.div`
  text-align: center;
`;

const EditColumn = styled.div`
  position: relative;
  .anticon {
    top: -10px;
    top: -0.625rem;
    &:hover svg path {
      fill: ${colors.blue};
      transition: fill 0.3s;
    }
  }
`;

const PipelineItem = ({
  uuid, name, last_pipeline_run, openPipelineEdit, viewPipelineRuns,
}) => {
  const lastPipelineRunState = (
    last_pipeline_run
      && last_pipeline_run.states
      && last_pipeline_run.states.length
      && last_pipeline_run.states[last_pipeline_run.states.length - 1]
  );

  const runStatus = lastPipelineRunState && lastPipelineRunState.state;

  return (
    <PipelineItemGrid gridTemplateColumns="1fr 48px 2fr 140px 40px" bgcolor="white">
      <StyledText
        aria-label="Pipeline Item name"
        size="xlarge"
        fontweight={700}
        color="black"
      >
        {name}
      </StyledText>
      <StatusLegend
        color={STATUS_LEGEND[runStatus]}
        title={STATUS_NAME_LEGEND[runStatus]}
      />
      <StyledText size="middle" color="darkText">
        {runStatus && `Last run ${STATUS_PHRASE_LEGEND[runStatus]} ${moment.utc(lastPipelineRunState && lastPipelineRunState.created_at).fromNow()}`}
      </StyledText>
      <ViewRunsColumn>
        <StyledButton
          aria-label={`${name} View Runs button`}
          size="middle"
          color="blue"
          width={108}
          onClick={() => viewPipelineRuns(uuid)}
        >
          View Runs
        </StyledButton>
      </ViewRunsColumn>
      <EditColumn>
        <EditOutlined onClick={() => openPipelineEdit(uuid)} />
      </EditColumn>
    </PipelineItemGrid>
  );
};

PipelineItem.propTypes = {
  uuid: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  last_pipeline_run: PropTypes.shape({
    states: PropTypes.arrayOf(PropTypes.shape({
      state: PropTypes.string.isRequired,
      created_at: PropTypes.string.isRequired,
    })),
  }),
  openPipelineEdit: PropTypes.func.isRequired,
  viewPipelineRuns: PropTypes.func.isRequired,
};

PipelineItem.defaultProps = {
  last_pipeline_run: null,
};

export default PipelineItem;
