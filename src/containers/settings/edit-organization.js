import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import styled from 'styled-components';

import { requestUpdateOrganization } from 'services';
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
    }
  }
  input {
    &.unfocusable {
      pointer-events: none;
    }  
  }
`;

const FormMessage = styled.div`
  text-align: right;
`;

const EditOrganization = () => {
  const [selectedOrganization, setSelectedOrganization] = useState(null);
  const [selectedOrganizationName, setSelectedOrganizationName] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const profile = useSelector((state) => state.user.profile);

  if (!profile) return null;

  const onOrganizationClick = (organizationUUID) => {
    setSelectedOrganization(organizationUUID);
  };

  const setOrganizationName = (e) => {
    setSelectedOrganizationName(e.target.value);
  };

  const onSaveClicked = (e) => {
    e.preventDefault();
    setLoading(true);

    if (!loading) {
      requestUpdateOrganization(selectedOrganization, selectedOrganizationName)
        .then(() => {
          setSelectedOrganization(null);
          setSelectedOrganizationName(null);
          setError(false);
          setLoading(false);
        })
        .catch(() => {
          setError(true);
          setLoading(false);
        });
    }
  };

  return (
    <StyledForm onSubmit={onSaveClicked}>
      {profile.organizations.map((org) => ( // TODO: org.role.name === ROLE_ADMINISTRATOR
        <>
          <label key={org.uuid} htmlFor={org.uuid}>
            <StyledText display="block" color="darkText">{org.name}</StyledText>
            <StyledInput
              type="text"
              bgcolor="white"
              size="large"
              className={org.uuid === selectedOrganization ? '' : 'unfocusable'}
              name={org.uuid}
              id={org.uuid}
              value={org.name}
              tabIndex={-1}
              onChange={setOrganizationName}
              onClick={() => onOrganizationClick(org.uuid)}
            />
            {org.uuid !== selectedOrganization && <EditOutlined />}
            {org.uuid === selectedOrganization && <DeleteOutlined />}
          </label>
          {org.uuid === selectedOrganization && (
          <FormMessage>
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
        </>
      ))}
    </StyledForm>
  );
};

export default EditOrganization;
