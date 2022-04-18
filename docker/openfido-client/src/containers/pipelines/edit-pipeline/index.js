import React, { useEffect, useState } from 'react';
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
  const [fields, setFields] = useState({
    name: pipelineItem && pipelineItem.name,
    description: pipelineItem && pipelineItem.description,
    docker_image_url: pipelineItem && pipelineItem.docker_image_url,
    repository_ssh_url: pipelineItem && pipelineItem.repository_ssh_url,
    repository_branch: pipelineItem && pipelineItem.repository_branch,
    repository_script: pipelineItem && pipelineItem.repository_script,
  });
  const [errors, setErrors] = useState({});
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showDeletePopup, setShowDeletePopup] = useState(false);
  const [hasBeenDeleted, setHasBeenDeleted] = useState(false);

  const currentOrg = useSelector((state) => state.user.currentOrg);

  useEffect(() => {
    if (formSubmitted && !errors.length && !loading) {
      setLoading(true);
      setFormSubmitted(false);

      requestUpdatePipeline(currentOrg, pipelineItem && pipelineItem.uuid, fields)
        .then(() => {
          handleSuccess();
          setErrors({});
          setLoading(false);
        })
        .catch(() => {
          setLoading(false);
        });
    }
  }, [formSubmitted, errors, currentOrg, fields, handleSuccess, loading, pipelineItem]);

  const validateField = (fieldName, fieldValue) => {
    let result;

    switch (fieldName) {
      case 'description':
        result = true; // optional
        break;
      case 'docker_image_url':
        result = fieldValue && fieldValue.length > 0;
        break;
      case 'repository_ssh_url':
        result = fieldValue && fieldValue.match(/^https:\/\/.+/i);
        break;
      case 'repository_script':
        result = fieldValue && fieldValue.match(/^.+\.sh$/i);
        break;
      default:
        result = fieldValue && fieldValue.length > 0;
        break;
    }
    return result;
  };

  const validateFields = () => {
    const fieldErrors = {};
    let result = true;

    Object.keys(fields).forEach((field) => {
      if (!validateField(field, fields[field])) {
        fieldErrors[field] = true;
        result = false;
      }
    });

    setErrors(fieldErrors);

    return result;
  };

  const onFieldChanged = (e, fieldName) => {
    setFields({
      ...fields,
      [fieldName]: e.target.value,
    });
  };

  const onFieldBlur = (e, fieldName) => {
    if (!validateField(fieldName, e.target.value)) {
      setErrors({
        ...errors,
        [fieldName]: true,
      });
    } else {
      const updatedErrors = { ...errors };
      delete updatedErrors[fieldName];
      setErrors(updatedErrors);
    }
  };

  const onEditPipelineClicked = (e) => {
    e.preventDefault();

    const result = validateFields();

    if (result) setFormSubmitted(true);

    return result;
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
          <label htmlFor="name" style={{ width: '100%' }}>
            <StyledText
              display="block"
              color={errors.name ? 'pink' : 'darkText'}
            >
              Pipeline Name
            </StyledText>
            <StyledInput
              type="text"
              bgcolor="white"
              size="large"
              name="name"
              id="name"
              value={fields.name}
              onBlur={(e) => onFieldBlur(e, 'name')}
              onChange={(e) => onFieldChanged(e, 'name')}
            />
          </label>
          <label htmlFor="description" style={{ width: '100%' }}>
            <StyledText
              display="block"
              color={errors.description ? 'pink' : 'darkText'}
            >
              Description
            </StyledText>
            <StyledTextArea
              rows={3}
              bgcolor="white"
              size="large"
              name="description"
              id="description"
              value={fields.description}
              onBlur={(e) => onFieldBlur(e, 'description')}
              onChange={(e) => onFieldChanged(e, 'description')}
            />
          </label>
          <label htmlFor="docker_image_url" style={{ width: '100%' }}>
            <StyledText
              display="block"
              color={errors.docker_image_url ? 'pink' : 'darkText'}
            >
              DockerHub Repository
            </StyledText>
            <StyledInput
              type="text"
              bgcolor="white"
              size="large"
              name="docker_image_url"
              id="docker_image_url"
              value={fields.docker_image_url}
              onBlur={(e) => onFieldBlur(e, 'docker_image_url')}
              onChange={(e) => onFieldChanged(e, 'docker_image_url')}
            />
          </label>
          <label htmlFor="repository_ssh_url" style={{ width: '100%' }}>
            <StyledText
              display="block"
              color={errors.repository_ssh_url ? 'pink' : 'darkText'}
            >
              Git Clone URL (https)
            </StyledText>
            <StyledInput
              type="text"
              bgcolor="white"
              size="large"
              name="repository_ssh_url"
              id="repository_ssh_url"
              value={fields.repository_ssh_url}
              onBlur={(e) => onFieldBlur(e, 'repository_ssh_url')}
              onChange={(e) => onFieldChanged(e, 'repository_ssh_url')}
            />
          </label>
          <label htmlFor="repository_branch" style={{ width: '100%' }}>
            <StyledText
              display="block"
              color={errors.repository_branch ? 'pink' : 'darkText'}
            >
              Repository Branch
            </StyledText>
            <StyledInput
              type="text"
              bgcolor="white"
              size="large"
              name="repository_branch"
              id="repository_branch"
              value={fields.repository_branch}
              onBlur={(e) => onFieldBlur(e, 'repository_branch')}
              onChange={(e) => onFieldChanged(e, 'repository_branch')}
            />
          </label>
          <label htmlFor="repository_script" style={{ width: '100%' }}>
            <StyledText
              display="block"
              color={errors.repository_script ? 'pink' : 'darkText'}
            >
              Entrypoint Script (.sh)
            </StyledText>
            <StyledInput
              type="text"
              bgcolor="white"
              size="large"
              name="repository_script"
              id="repository_script"
              value={fields.repository_script}
              onBlur={(e) => onFieldBlur(e, 'repository_script')}
              onChange={(e) => onFieldChanged(e, 'repository_script')}
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
              Update Pipeline
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
    repository_script: PropTypes.string.isRequired,
  })).isRequired,
};

export default EditPipeline;
