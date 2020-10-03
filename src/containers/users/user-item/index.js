import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Dropdown, Menu } from 'antd';
import styled from 'styled-components';
import moment from 'moment';

import { removeOrganizationMember } from 'actions/organization';
import DownOutlined from 'icons/DownOutlined';
import DeleteOutlined from 'icons/DeleteOutlined';
import {
  StyledGrid,
  StyledText,
} from 'styles/app';
import colors from 'styles/colors';

const StyledDropdown = styled(Dropdown)`
  position: relative;
  &.ant-dropdown-trigger {
    width: 112px;
    display: inline-flex;
    justify-content: space-between;
  }
  .ant-dropdown-menu {
    left: -20px;
  }
`;

const DeleteColumn = styled.div`
  position: relative;
  .anticon {
    left: 0;
    top: -14px;
    top: -0.875rem;
  }
`;

const StyledMenu = styled(Menu)`
  display: block;
  width: 169px;
  margin: 0 auto;
  background: ${colors.white};
  padding: 16px 0;
  padding: 1rem 0;
  border-radius: 3px;
  box-shadow: none;
  border: 0.5px solid ${colors.lightGray};
  color: ${colors.gray};
  text-align: center;
  position: relative;
  left: -32px;
  left: -2rem;
  li:first-child {
    font-size: 12px;
    line-height: 14px;
    text-align: center;
  }
  li:not(.ant-dropdown-menu-item) {
    margin: 8px 16px;
    margin: 0.5rem 1rem;
    font-size: 12px;
    font-size: 0.75rem;
    line-height: 14px;
    line-height: 0.875rem;
  }
`;

const StyledMenuItem = styled(Menu.Item)`
  color: ${colors.gray};
  font-size: 14px;
  line-height: 16px;
  font-weight: 500;
  border: 1px solid ${colors.lightBorder};
  border-radius: 3px;
  padding: 6px 8px;
  margin: 0 32px;
  &:hover {
    background-color: ${colors.blue};
    border-color: transparent;
    color: ${colors.white};
  }
  &:first-of-type {
    margin-top: 16px;
    margin-top: 1rem;
  }
  &:not(:last-child) {
    margin-bottom: 10px;
    margin-bottom: 0.625rem;
   }
`;

const User = ({
  first_name, last_name, is_system_admin, last_active_at,
}) => {
  const [userRole, setUserRole] = useState(is_system_admin ? 'Administrator' : 'Unassigned');
  const dispatch = useDispatch();

  const onDeleteUserClicked = (user_uuid) => {
    dispatch(removeOrganizationMember(user_uuid));
  }

  const menu = (
    <StyledMenu>
      <li>
        <StyledText size="large" fontweight={500}>Change role</StyledText>
      </li>
      <StyledMenuItem onClick={() => setUserRole('Administrator')}>
        <span>Administrator</span>
      </StyledMenuItem>
      <li>
        Able to manage <strong>Users</strong>, <strong>Pipelines</strong>, <strong>Files</strong> for this organization.
      </li>
      <StyledMenuItem onClick={() => setUserRole('Engineer')}>
        <span>Engineer</span>
      </StyledMenuItem>
      <li>
        Able to manage <strong>Pipelines</strong> and <strong>Files</strong> for this organization.
      </li>
      <StyledMenuItem onClick={() => setUserRole('Unassigned')}>
        <span>Unassigned</span>
      </StyledMenuItem>
      <li>View only.</li>
    </StyledMenu>
  );

  return (
    <StyledGrid gridTemplateColumns="3fr 2fr 2fr 1fr" bgcolor="white">
      <StyledText size="large" color="gray">
        {first_name}
        {last_name && ` ${last_name}`}
      </StyledText>
      <StyledDropdown overlay={menu} trigger="click">
        <StyledText size="large" color="gray">
          {userRole}
          <DownOutlined color="lightGray" />
        </StyledText>
      </StyledDropdown>
      <StyledText size="large" color="gray">
        {moment(last_active_at).fromNow()}
      </StyledText>
      <DeleteColumn>
        <DeleteOutlined color="gray20" onClick={onDeleteUserClicked} />
      </DeleteColumn>
    </StyledGrid>
  );
};

export default User;
