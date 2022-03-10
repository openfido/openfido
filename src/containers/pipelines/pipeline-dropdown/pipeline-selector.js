import React from 'react';

const PipelineSelector = ({ pipeline, updateFromDropdown }) => {
// assign required values to each element for click handler
  console.log(pipeline, updateFromDropdown.updateFromDropdown);
  return (
    <option
      id={pipeline.id}
      data-url={pipeline.url}
      data-fullname={pipeline.full_name}
      onClick={(e) => {
        updateFromDropdown.updateFromDropdown(e);
      }}
    >
      {pipeline.full_name}
    </option>
  );
};

export default PipelineSelector;
