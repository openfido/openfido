import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useSelector } from 'react-redux';
import styled from 'styled-components';
import { Space } from 'antd';

import { requestCreatePipeline } from 'services';
import {
  StyledH3,
  StyledButton, StyledText, StyledInput, StyledTextArea,
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

const AddPipeline = ({ handleSuccess, handleCancel }) => {
  const [fields, setFields] = useState({
    name: '',
    description: '',
    docker_image_url: '',
    repository_ssh_url: '',
    repository_branch: '',
    script: 'openfido.sh',
  });
  const [errors, setErrors] = useState({});
  const [formSubmitted, setFormSubmitted] = useState(false);

  const currentOrg = useSelector((state) => state.user.currentOrg);

  useEffect(() => {
    if (formSubmitted && !errors.length) {
      requestCreatePipeline(currentOrg, fields)
        .then(() => {
          handleSuccess();
          setErrors({});
          setFormSubmitted(false);
        })
        .catch(() => {
          setFormSubmitted(false);
        });
    }
  }, [formSubmitted, errors, currentOrg, fields, handleSuccess]);

  const validateField = (fieldName, fieldValue) => {
    let result;

    switch (fieldName) {
      case 'description':
        result = true; // optional
        break;
      case 'docker_image_url':
        result = fieldValue && fieldValue.match(/^http(s)?:\/\/.+/i);
        break;
      case 'repository_ssh_url':
        result = fieldValue && fieldValue.match(/^https:\/\/.+/i);
        break;
      case 'script':
        result = fieldValue && fieldValue.match(/\.sh$/i);
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

  const onAddPipelineClicked = (e) => {
    e.preventDefault();

    const result = validateFields();

    if (result) setFormSubmitted(true);

    return result;
  };

  const onCancelClicked = () => {
    handleCancel();
  };

  return (
    <AddPipelineForm onSubmit={onAddPipelineClicked}>
      <StyledH3 color="black">Add a pipeline</StyledH3>
      <Space direction="vertical" size={24}>
        <label htmlFor="name">
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
        <label htmlFor="description">
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
        <label htmlFor="docker_image_url">
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
        <label htmlFor="repository_ssh_url">
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
        <label htmlFor="repository_branch">
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
        <label htmlFor="script">
          <StyledText
            display="block"
            color={errors.script ? 'pink' : 'darkText'}
          >
            Entrypoint Script (.sh)
          </StyledText>
          <StyledInput
            type="text"
            bgcolor="white"
            size="large"
            name="script"
            id="script"
            value={fields.script}
            onBlur={(e) => onFieldBlur(e, 'script')}
            onChange={(e) => onFieldChanged(e, 'script')}
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

AddPipeline.propTypes = {
  handleSuccess: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
};

export default AddPipeline;
