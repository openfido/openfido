import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const Button = styled.button`
background: none!important;
border: none;
padding: 0!important;
width: 100%;
text-align: left;
`;

const StyledContainer = styled.div`
:hover {
  background-color: yellow;
};
`;

const PipelineSelector = (props) => {
// assign required values to each element for click handler
// OPTION element doesn't work correctly in Safari, had to use workaround for compatability
  const { pipeline, updateFromDropdown } = props;
  return (
    <StyledContainer>
      <Button
        type="button"
        role="menuitem"
        id={pipeline.id}
        data-url={pipeline.url}
        data-fullname={pipeline.full_name}
        data-description={pipeline.description}
        onClick={(e) => {
          updateFromDropdown.updateFromDropdown(e);
        }}
      >
        {pipeline.full_name.charAt(0).toUpperCase() + pipeline.full_name.slice(1)}
      </Button>
    </StyledContainer>
  );
};

PipelineSelector.propTypes = {
  pipeline: PropTypes.shape({
    id: PropTypes.oneOfType([
      PropTypes.string,
      PropTypes.number,
    ]).isRequired,
    url: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    full_name: PropTypes.string.isRequired,
  }).isRequired,
  updateFromDropdown: PropTypes.shape({
    updateFromDropdown: PropTypes.func.isRequired,
  }).isRequired,

};

export default PipelineSelector;
