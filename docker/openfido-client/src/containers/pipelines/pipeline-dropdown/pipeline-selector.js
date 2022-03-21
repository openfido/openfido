import React from 'react';

const PipelineSelector = (props) => {
// assign required values to each element for click handler
  const { pipeline, updateFromDropdown } = props;
  return (
    <option
      id={pipeline.id}
      data-url={pipeline.url}
      data-fullname={pipeline.full_name}
      data-description={pipeline.description}
      onClick={(e) => {
        updateFromDropdown.updateFromDropdown(e);
      }}
    >
      {pipeline.full_name}
    </option>
  );
};

export default PipelineSelector;
