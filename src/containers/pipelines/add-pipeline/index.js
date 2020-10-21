import React, { useState } from 'react';
import styled from 'styled-components';
import { Space } from 'antd';

import {
  StyledH3, StyledText, StyledInput, StyledTextArea, StyledButton,
} from 'styles/app';

const AddPipelineForm = styled.form`
  max-width: 432px;
  h3 {
    margin-bottom: 32px;
    margin-bottom: 2rem;
  }
  padding: 24px 18px;
  padding: 1.5rem 1rem;
`;

const AddPipeline = () => {
  const [pipelineName, setPipelineName] = useState('');
  const [description, setDescription] = useState('');
  const [dockerImageUrl, setDockerImageUrl] = useState('');
  const [repositorySshUrl, setRepositorySshUrl] = useState('');
  const [repositoryBranch, setRepositoryBranch] = useState('');

  const onAddPipelineClicked = (e) => {
    e.preventDefault();
  };

  const onCancelClicked = () => {
    setPipelineName('');
    setDescription('');
    setDockerImageUrl('');
    setRepositorySshUrl('');
    setRepositoryBranch('');
  };

  return (
    <AddPipelineForm onSubmit={onAddPipelineClicked}>
      <StyledH3 color="black">Add a pipeline</StyledH3>
      <Space direction="vertical" size={24}>
        <label htmlFor="pipeline_name">
          <StyledText display="block" color="darkText">Pipeline Name</StyledText>
          <StyledInput
            type="text"
            bgcolor="white"
            size="large"
            name="pipeline_name"
            id="pipeline_name"
            value={pipelineName}
            onChange={(e) => setPipelineName(e.target.value)}
          />
        </label>
        <label htmlFor="description">
          <StyledText display="block" color="darkText">Description</StyledText>
          <StyledTextArea
            rows={3}
            bgcolor="white"
            size="large"
            name="description"
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </label>
        <label htmlFor="docker_image_url">
          <StyledText display="block" color="darkText">DockerHub Repository</StyledText>
          <StyledInput
            type="text"
            bgcolor="white"
            size="large"
            name="docker_image_url"
            id="docker_image_url"
            value={dockerImageUrl}
            onChange={(e) => setDockerImageUrl(e.target.value)}
          />
        </label>
        <label htmlFor="repository_ssh_url">
          <StyledText display="block" color="darkText">Github Repository</StyledText>
          <StyledInput
            type="text"
            bgcolor="white"
            size="large"
            name="repository_ssh_url"
            id="repository_ssh_url"
            value={repositorySshUrl}
            onChange={(e) => setRepositorySshUrl(e.target.value)}
          />
        </label>
        <label htmlFor="repository_branch">
          <StyledText display="block" color="darkText">Github Repository Branch</StyledText>
          <StyledInput
            type="text"
            bgcolor="white"
            size="large"
            name="repository_branch"
            id="repository_branch"
            value={repositoryBranch}
            onChange={(e) => setRepositoryBranch(e.target.value)}
          />
        </label>
        <Space direction="horizontal" size={24}>
          <StyledButton
            htmlType="submit"
            size="middle"
            color="blue"
            width={141}
            role="button"
            tabIndex={0}
            onClick={onAddPipelineClicked}
          >
            Add Pipeline
          </StyledButton>
          <StyledButton
            htmlType="reset"
            type="text"
            height={50}
            onClick={onCancelClicked}
          >
            Cancel
          </StyledButton>
        </Space>
      </Space>
    </AddPipelineForm>
  );
};

export default AddPipeline;
