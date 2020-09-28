import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Space } from 'antd';
import PropTypes from 'prop-types';

import { getPipelines as getPipelinesAction } from 'actions/pipelines';
import { StyledTitle, StyledButton } from 'styles/app';
import PipelineItem from './PipelineItem';

function Pipelines({ getPipelines, pipelines }) {
  useEffect(() => {
    getPipelines();
  }, [getPipelines]);

  return (
    <>
      <StyledTitle>
        <div>
          <h1>Pipelines</h1>
          <StyledButton size="small">
            + Add Pipeline
          </StyledButton>
        </div>
      </StyledTitle>
      <Space direction="vertical" size={16}>
        {pipelines.map(({ id, name, last_updated: lastUpdated }) => (
          <PipelineItem key={id} id={id} name={name} lastUpdated={lastUpdated} />
        ))}
      </Space>
    </>
  );
}

Pipelines.propTypes = {
  getPipelines: PropTypes.func.isRequired,
  pipelines: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired,
    last_updated: PropTypes.string.isRequired,
  })).isRequired,
};

const mapStateToProps = (state) => ({
  pipelines: state.pipelines.pipelines,
});

const mapDispatch = (dispatch) => bindActionCreators({
  getPipelines: getPipelinesAction,
}, dispatch);

export default connect(mapStateToProps, mapDispatch)(Pipelines);
