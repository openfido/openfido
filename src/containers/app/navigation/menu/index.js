import React from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';
import styled from 'styled-components';
import { Menu } from 'antd';

import {
  ROUTE_PIPELINES,
  ROUTE_USERS,
  ROUTE_SETTINGS,
} from 'config/routes';
import colors from 'styles/colors';

const StyledMenu = styled(Menu)`
  padding: 23px 9px 0 0;
  &.ant-menu-vertical {
    border-right: 0;
    .ant-menu-item-selected {
      background-color: ${colors.black};
      color: ${colors.white};
      cursor: default;
    }
     > .ant-menu-item {
    margin: 0;
    height: auto;
    line-height: 47px;
  }
`;

const StyledMenuItem = styled(Menu.Item)`
  padding-left: 16px 13px; 
  font-size: 16px;
  font-weight: 500;
  text-transform: uppercase;
  border-radius: 2px;
  &, &:hover {
    color: #404040;
  }
  &:hover {
    background-color: ${colors.lightGray};
  }
`;

const MainMenu = () => {
  const history = useHistory();
  const navigate = (path) => (() => history.push(path));
  const location = useLocation();
  const path = location.pathname;

  const profile = useSelector((state) => state.user.profile);
  if (!profile) return null;

  const selectedKeys = [];
  if (path.includes(ROUTE_PIPELINES)) selectedKeys.push('pipelines');
  if (path.includes(ROUTE_USERS)) selectedKeys.push('users');
  if (path.includes(ROUTE_SETTINGS)) selectedKeys.push('jobs');

  return (
    <StyledMenu selectedKeys={selectedKeys}>
      <StyledMenuItem key="pipelines" onClick={navigate(ROUTE_PIPELINES)}>Pipelines</StyledMenuItem>
      {profile.is_system_admin && <StyledMenuItem key="users" onClick={navigate(ROUTE_USERS)}>Users</StyledMenuItem>}
      <StyledMenuItem key="settings" onClick={navigate(ROUTE_SETTINGS)}>Settings</StyledMenuItem>
    </StyledMenu>
  );
};

export default MainMenu;
