import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Space } from 'antd';
import styled from 'styled-components';

import { requestUserOrganizations } from 'services';
import { updateUserProfile, updateUserAvatar } from 'actions/user';
import { StyledText, StyledInput, StyledButton } from 'styles/app';
import EditOutlined from 'icons/EditOutlined.js';
import DeleteOutlined from 'icons/DeleteOutlined.js';
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
  const [selectedOrganizationName, setSelectedOrganizationName] = useState('');
  const profile = useSelector((state) => state.user.profile);
  const dispatch = useDispatch();

  if (!profile) return null;

  const onOrganizationClick = (organizationName) => {
    setSelectedOrganization(organizationName);
  };

  const setOrganizationName = (e) => {
    setSelectedOrganizationName(e.target.value);
  };

  const onSaveClicked = () => {

  };

  return (
    <StyledForm onSubmit={onSaveClicked}>
      {profile.organizations.map((org) => ( // TODO: org.role.name === ROLE_ADMINISTRATOR
        <>
          <label key={org.name} htmlFor={org.name}>
            <StyledText display="block" color="darkText">{org.name}</StyledText>
            <StyledInput
              type="text"
              bgcolor="white"
              size="large"
              className={org.name === selectedOrganization ? '' : 'unfocusable'}
              name={org.name}
              id={org.name}
              value={org.name}
              tabIndex={-1}
              onChange={setOrganizationName}
              onClick={() => onOrganizationClick(org.name)}
            />
            {org.name !== selectedOrganization && <EditOutlined />}
            {org.name === selectedOrganization && <DeleteOutlined />}
          </label>
          {org.name === selectedOrganization && (
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
