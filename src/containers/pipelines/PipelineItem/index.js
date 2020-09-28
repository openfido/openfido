import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Dropdown } from 'antd';

import {
  deletePipeline as deletePipelineAction,
} from 'actions/pipelines';
import DownOutlined from 'icons/DownOutlined';
import {
  StyledGrid,
  StyledMenu,
  StyledMenuItem,
  StyledButton,
  StyledText,
} from 'styles/app';

const Pipeline = ({
  id, name, lastUpdated, deletePipeline,
}) => {
  const menu = (
    <StyledMenu>
      <StyledMenuItem>
        <span>View Latest Output</span>
      </StyledMenuItem>
      <StyledMenuItem>
        <span>Update Now</span>
      </StyledMenuItem>
      <StyledMenuItem hovercolor="orangeRed" onClick={() => deletePipeline({ id })}>
        <span>Delete</span>
      </StyledMenuItem>
    </StyledMenu>
  );

  return (
    <StyledGrid gridTemplateColumns="1fr 1fr 0.25fr 0.5fr" bgcolor="white">
      <StyledText size="large" fontweight={500} color="blue">
        {name}
      </StyledText>
      <StyledText size="middle" fontweight={500} color="darkGray">
        {`Last updated ${lastUpdated}`}
      </StyledText>
      <Dropdown overlay={menu}>
        <StyledButton size="large" width={134} color="green">
          <StyledText>Succeeded</StyledText>
          <DownOutlined />
        </StyledButton>
      </Dropdown>
    </StyledGrid>
  );
};

Pipeline.propTypes = {
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
  lastUpdated: PropTypes.string.isRequired,
  deletePipeline: PropTypes.func.isRequired,
};

const mapDispatch = (dispatch) => bindActionCreators({
  deletePipeline: deletePipelineAction,
}, dispatch);

export default connect(undefined, mapDispatch)(Pipeline);
