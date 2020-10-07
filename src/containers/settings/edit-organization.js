import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { requestUpdateOrganization, requestDeleteOrganization } from 'services';
import { getUserOrganizations } from 'actions/user';
import { StyledText, StyledInput, StyledButton } from 'styles/app';
import EditOutlined from 'icons/EditOutlined';
import DeleteOutlined from 'icons/DeleteOutlined';
import colors from 'styles/colors';

const StyledForm = styled.form`
  display: grid;
  grid-gap: 16px;
  grid-gap: 1rem;
  width: 432px;
  label {
    position: relative;
    cursor: pointer;
    &:hover {
      svg path {
        fill: ${colors.blue};
      }
      .anticon-delete-outlined svg path {
        fill: ${colors.pink};
      }
    }
    button {
      margin-top: 8px;
      margin-top: 0.5rem;
  }
  .anticon {
    top: auto;
    bottom: 16px;
    bottom: 1rem;
    right: 16px;
    right: 1rem;
    &.anticon-delete-outlined {
      right: -32px;
      right: -2rem;
      bottom: 48px;
      bottom: 3rem;
    }
  }
  input {
    &.unfocusable {
      pointer-events: none;
    }  
  }
`;

const FormMessage = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const EditOrganization = () => {
  const [selectedOrganization, setSelectedOrganization] = useState(null);
  const [selectedOrganizationName, setSelectedOrganizationName] = useState(null);
  const [selectedInput, setSelectedInput] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const profile = useSelector((state) => state.user.profile);
  const dispatch = useDispatch();

  if (!profile) return null;

  const onOrganizationClick = (e, organizationUUID, organizationName) => {
    setSelectedOrganization(organizationUUID);
    setSelectedOrganizationName(organizationName);
    setSelectedInput(e.target);
  };

  const setOrganizationName = (e) => {
    setSelectedOrganizationName(e.target.value);
  };

  const onSaveClicked = (e) => {
    e.preventDefault();

    if (!loading) {
      setLoading(true);
      requestUpdateOrganization(selectedOrganization, selectedOrganizationName)
        .then(() => {
          setSelectedOrganization(null);
          setSelectedOrganizationName(null);
          setError(null);
          setLoading(false);
          if (selectedInput) selectedInput.blur();
          setSelectedInput(null);
          dispatch(getUserOrganizations(profile.uuid));
        })
        .catch(() => {
          setError('save');
          setLoading(false);
        });
    }
  };

  const onDeleteClicked = () => {
    if (!loading) {
      setLoading(true);
      requestDeleteOrganization(selectedOrganization)
        .then(() => {
          setSelectedOrganization(null);
          setSelectedOrganizationName(null);
          setError(null);
          setLoading(false);
          if (selectedInput) selectedInput.blur();
          setSelectedInput(null);
          dispatch(getUserOrganizations(profile.uuid));
        })
        .catch(() => {
          setError('delete');
          setLoading(false);
        });
    }
  };

  return (
    <StyledForm onSubmit={onSaveClicked}>
      {profile.organizations.map((org) => ( // TODO: org.role.name === ROLE_ADMINISTRATOR
        <label
          key={org.uuid}
          htmlFor={org.uuid}
        >
          <StyledText display="block" color="darkText">{org.name}</StyledText>
          <StyledInput
            type="text"
            bgcolor="white"
            size="large"
            className={org.uuid === selectedOrganization ? '' : 'unfocusable'}
            name={org.uuid}
            id={org.uuid}
            value={org.uuid === selectedOrganization ? selectedOrganizationName : org.name}
            tabIndex={-1}
            onChange={setOrganizationName}
            onClick={(e) => onOrganizationClick(e, org.uuid, org.name)}
          />
          {org.uuid !== selectedOrganization && <EditOutlined />}
          {org.uuid === selectedOrganization && <DeleteOutlined onClick={onDeleteClicked} />}
          {org.uuid === selectedOrganization && (
          <FormMessage>
            <StyledText color="pink">
              {error === 'save' && 'Could not save organization name.'}
              {error === 'delete' && 'Could not delete organization.'}
            </StyledText>
            <StyledButton
              htmlType="submit"
              color="lightBlue"
              hoverbgcolor="blue"
              width={50}
              onClick={onSaveClicked}
            >
              <span>Save</span>
            </StyledButton>
          </FormMessage>
          )}
        </label>
      ))}
    </StyledForm>
  );
};

export default EditOrganization;
