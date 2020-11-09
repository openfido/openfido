import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Space } from 'antd';
import styled from 'styled-components';

import { StyledButton, StyledInput } from 'styles/app';

const PopupButton = styled(StyledButton)`
  margin: 20px auto 0 auto;
  margin: 1.25rem auto 0 auto;
`;

const AddImageStep = ({ selectedArtifact, onNextClicked }) => {
  const [title, setTitle] = useState('');

  const onAddChartClicked = (e) => {
    e.preventDefault();
    onNextClicked(title);
  };

  return (
    <form onSubmit={onAddChartClicked}>
      <Space direction="vertical" size={24}>
        <StyledInput
          size="middle"
          placeholder="Edit Name of Image"
          bgcolor="white"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        {selectedArtifact && selectedArtifact.url && (
          <img src={selectedArtifact.url} alt={selectedArtifact.name} width="100%" />
        )}
      </Space>
      <PopupButton size="middle" color="blue" width={108} onClick={onAddChartClicked}>
        Add Chart
      </PopupButton>
    </form>
  );
};

AddImageStep.propTypes = {
  selectedArtifact: PropTypes.shape({
    name: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
    uuid: PropTypes.string.isRequired,
  }).isRequired,
  onNextClicked: PropTypes.func.isRequired,
};

export default AddImageStep;
