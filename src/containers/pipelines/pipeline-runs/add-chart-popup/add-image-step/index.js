import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Space } from 'antd';
import { CHART_TITLE_LENGTH_LIMIT } from 'config/charts';
import colors from 'styles/colors';
import styled from 'styled-components';

import { PopupButton } from 'styles/pipeline-runs';
import { StyledInput } from 'styles/app';

const ConfigChartForm = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  section {
    border-radius: 6px;
    background-color: ${colors.white};
    min-height: 231px;
    padding: 2rem 0 0 1rem;
  }
  > button {
    margin: 24px auto 0 auto;
    margin: 1.5rem auto 0 auto;
  }
  input.invalid {
    &::placeholder {
      color: ${colors.pink};
    }
  }
`;

const AddImageStep = ({ selectedArtifact, onNextClicked }) => {
  const [title, setTitle] = useState('');
  const [titleError, setTitleError] = useState(false);

  const onAddChartClicked = () => {
    if (title && title.length && title.length < CHART_TITLE_LENGTH_LIMIT) {
      onNextClicked(title);
      setTitleError(false);
    } else {
      setTitleError(true);
    }
  };

  return (
    <ConfigChartForm onSubmit={onAddChartClicked}>
      <Space direction="vertical" size={24}>
        <StyledInput
          size="middle"
          placeholder="Edit Name of Image"
          bgcolor="white"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className={titleError && 'invalid'}
        />
        {selectedArtifact && selectedArtifact.url && (
          <img src={selectedArtifact.url} alt={selectedArtifact.name} width="100%" />
        )}
      </Space>
      <PopupButton size="middle" color="blue" width={108} onClick={onAddChartClicked}>
        Add Chart
      </PopupButton>
    </ConfigChartForm>
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
