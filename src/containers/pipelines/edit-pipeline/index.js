import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useSelector } from 'react-redux';
import styled from 'styled-components';
import { Space } from 'antd';

import { requestUpdatePipeline } from 'services';
import DeleteOutlined from 'icons/DeleteOutlined';
import {
  StyledH3, StyledText, StyledInput, StyledTextArea, StyledButton,
} from 'styles/app';
import colors from 'styles/colors';
import DeletePipelinePopup from '../delete-pipeline-popup';

const EditPipelineForm = styled.form`
  max-width: 432px;
  h3 {
    margin-bottom: 32px;
    margin-bottom: 2rem;
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    .ant-btn {
      height: 20px;
      color: ${colors.gray20};
      padding-right: 16px;
      padding-right: 1rem;
      &:hover {
        color: ${colors.pink};
      }
      svg path {
        transition: fill 0.3s cubic-bezier(.645,.045,.355,1);
      }
      &:hover svg path {
        fill: ${colors.pink};
      }
      &:focus>span, &:active>span {
        position: absolute;
      }
    }
  }
  padding: 24px 18px;
  padding: 1.5rem 1rem;
`;

const EditPipeline = ({ handleSuccess, handleCancel, pipelineItem }) => {
  const currentOrg = useSelector((state) => state.user.currentOrg);

  const [pipelineName, setPipelineName] = useState(pipelineItem && pipelineItem.name);
  const [description, setDescription] = useState(pipelineItem && pipelineItem.description);
  const [dockerImageUrl, setDockerImageUrl] = useState(pipelineItem && pipelineItem.docker_image_url);
  const [repositorySshUrl, setRepositorySshUrl] = useState(pipelineItem && pipelineItem.repository_ssh_url);
  const [repositoryBranch, setRepositoryBranch] = useState(pipelineItem && pipelineItem.repository_branch);
  const [showDeletePopup, setShowDeletePopup] = useState(false);
  const [hasBeenDeleted, setHasBeenDeleted] = useState(false);

  const onEditPipelineClicked = (e) => {
    e.preventDefault();

    if (pipelineItem && currentOrg) {
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
    }
  };

  const onCancelClicked = () => {
    handleCancel();
  };

  const openDeletePopup = () => {
    setShowDeletePopup(true);
  };

  const closeDeletePopup = () => {
    setShowDeletePopup(false);
  };

  const onPermanentlyDeleteClicked = () => {
    setShowDeletePopup(false);
    setHasBeenDeleted(true);
    handleSuccess();
  };

  if (hasBeenDeleted) return null;

  return (
    <>
      <EditPipelineForm onSubmit={onEditPipelineClicked}>
        <StyledH3 color="black">
          Edit Pipeline
          <StyledButton type="text" size="small" onClick={openDeletePopup} width={108}>
            Delete Pipeline
            <DeleteOutlined color="gray20" onClick={openDeletePopup} />
          </StyledButton>
        </StyledH3>
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
      {showDeletePopup && (
        <DeletePipelinePopup
          handleOk={onPermanentlyDeleteClicked}
          handleCancel={closeDeletePopup}
          pipelineUUID={pipelineItem.uuid}
          pipelineName={pipelineItem.name}
        />
      )}
    </>
  );
};

EditPipeline.propTypes = {
  handleSuccess: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
  pipelineItem: PropTypes.objectOf(PropTypes.shape({
    uuid: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    docker_image_url: PropTypes.string.isRequired,
    repository_ssh_url: PropTypes.string.isRequired,
    repository_branch: PropTypes.string.isRequired,
  })).isRequired,
};

export default EditPipeline;
