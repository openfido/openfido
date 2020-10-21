import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useSelector } from 'react-redux';
import styled from 'styled-components';
import { Space } from 'antd';

import { requestUpdatePipeline } from 'services';
import {
  StyledH3, StyledText, StyledInput, StyledTextArea, StyledButton,
} from 'styles/app';

const EditPipelineForm = styled.form`
  max-width: 432px;
  h3 {
    margin-bottom: 32px;
    margin-bottom: 2rem;
  }
  padding: 24px 18px;
  padding: 1.5rem 1rem;
`;

const EditPipeline = ({ handleSuccess, pipelineItem }) => {
  const currentOrg = useSelector((state) => state.user.currentOrg);

  const [pipelineName, setPipelineName] = useState(pipelineItem.name);
  const [description, setDescription] = useState(pipelineItem.description);
  const [dockerImageUrl, setDockerImageUrl] = useState(pipelineItem.docker_image_url);
  const [repositorySshUrl, setRepositorySshUrl] = useState(pipelineItem.repository_ssh_url);
  const [repositoryBranch, setRepositoryBranch] = useState(pipelineItem.repository_branch);

  const onEditPipelineClicked = (e) => {
    e.preventDefault();

    requestUpdatePipeline(currentOrg, pipelineItem.uuid, {
      name: pipelineName,
      description,
      docker_image_url: dockerImageUrl,
      repository_ssh_url: repositorySshUrl,
      repository_branch: repositoryBranch,
    })
      .then(() => {
        handleSuccess();
      })
      .catch(() => {

      });
  };

  const onCancelClicked = () => {
    setPipelineName('');
    setDescription('');
    setDockerImageUrl('');
    setRepositorySshUrl('');
    setRepositoryBranch('');
  };

  return (
    <EditPipelineForm onSubmit={onEditPipelineClicked}>
      <StyledH3 color="black">Edit pipeline</StyledH3>
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
            onClick={onEditPipelineClicked}
          >
            Edit Pipeline
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
    </EditPipelineForm>
  );
};

EditPipeline.propTypes = {
  handleSuccess: PropTypes.func.isRequired,
  pipelineItem: PropTypes.objectOf(PropTypes.shape({
    name: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    docker_image_url: PropTypes.string.isRequired,
    repository_ssh_url: PropTypes.string.isRequired,
    repository_branch: PropTypes.string.isRequired,
  })).isRequired,
};

export default EditPipeline;
