import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';
import styled from 'styled-components';
import { Menu } from 'antd';

import {
  ROUTE_PIPELINES,
  ROUTE_USERS,
  ROUTE_SETTINGS,
} from 'config/routes';
import { ROLE_ADMINISTRATOR } from 'config/roles';
import colors from 'styles/colors';

const StyledMenu = styled(Menu)`
  padding: 16px 10px 0 0;
  padding: 1rem 0.625rem 0 0;
  &.ant-menu-vertical {
    border-right: 0;
    > .ant-menu-item {
      height: auto;
      font-size: 16px;
      font-size: 1rem;
      line-height: 47px;
      font-weight: 500;
      text-transform: uppercase;
      border-radius: 2px;
      &, a {
        color: ${colors.black};
      }
      &:hover {
        background-color: ${colors.lightGray};
      }
      &.ant-menu-item-selected, &.ant-menu-item-selected:hover {
        background-color: ${colors.blue};
        &, a, a:hover {
          color: ${colors.white};
        }
      }
    }
`;

const MainMenu = () => {
  const location = useLocation();
  const path = location.pathname;

  const organizations = useSelector((state) => state.user.organizations);
  const currentOrg = useSelector((state) => state.user.currentOrg);

  const isOrganizationAdmin = currentOrg && organizations && organizations.find((org) => org.uuid === currentOrg && org.role.code === ROLE_ADMINISTRATOR.code);

  const selectedKeys = [];
  if (path.includes(ROUTE_PIPELINES)) selectedKeys.push('pipelines');
  if (path.includes(ROUTE_USERS)) selectedKeys.push('users');
  if (path.includes(ROUTE_SETTINGS)) selectedKeys.push('settings');

  return (
    <StyledMenu selectedKeys={selectedKeys}>
      {currentOrg && (
        <Menu.Item key="pipelines">
          <Link to={ROUTE_PIPELINES}>Pipelines</Link>
        </Menu.Item>
      )}
      {isOrganizationAdmin && (
        <Menu.Item key="users">
          <Link to={ROUTE_USERS}>Users</Link>
        </Menu.Item>
      )}
      <Menu.Item key="settings">
        <Link to={ROUTE_SETTINGS}>Settings</Link>
      </Menu.Item>
    </StyledMenu>
  );
};

export default MainMenu;
