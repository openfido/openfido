import React, { useState } from 'react';
import { useSelector } from 'react-redux';
import styled from 'styled-components';
import { Menu } from 'antd';

import { StyledTitle, StyledText } from 'styles/app';
import colors from 'styles/colors';
import EditProfile from './edit-profile';
import ChangePassword from './change-password';
import EditOrganization from './edit-organization';

const Root = styled.div`
  padding: 60px 90px;
  display: grid;
  grid-template-columns: 250px 1fr;
`;

const StyledMenu = styled(Menu)`
  background-color: transparent;
  border-right: 0;
  &.ant-menu:not(.ant-menu-horizontal) .ant-menu-item-selected {
    border-color: ${colors.blue};
    background-color: transparent;
    font-weight: bold;
    color: ${colors.blue};
  }
  .ant-menu-item {
    border-left: 1px solid transparent;
    height: 24px;
    height: 1.5rem;
    line-height: 24px;
    line-height: 1.5rem;
    padding: 0 8px;
    padding: 0 0.5rem;
    margin: 10px 0;
    margin: 0.625rem 0;
    font-weight: 500;
    color: ${colors.gray80};
    &:hover {
      color: ${colors.blue};
    }
    &:first-of-type {
      margin-top: 0;
    } 
  }
`;

const Settings = () => {
  const profile = useSelector((state) => state.user.profile);
  const [selectedKey, setSelectedKey] = useState('Edit Profile');

  if (!profile) return null;

  let content = null;
  switch (selectedKey) {
    case 'Edit Profile':
      content = <EditProfile />;
      break;
    case 'Change Password':
      content = <ChangePassword />;
      break;
    case 'Edit Organization':
      content = <EditOrganization />;
      break;
    default:
      break;
  }

  return (
    <>
      <StyledTitle>
        <h1>Settings</h1>
      </StyledTitle>
      <Root>
        <StyledMenu selectedKeys={[selectedKey]}>
          <Menu.Item key="Edit Profile" onClick={() => setSelectedKey('Edit Profile')}>
            <StyledText size="xlarge">Edit Profile</StyledText>
          </Menu.Item>
          <Menu.Item key="Change Password" onClick={() => setSelectedKey('Change Password')}>
            <StyledText size="xlarge">Change Password</StyledText>
          </Menu.Item>
          {profile.is_system_admin && (
          <Menu.Item key="Edit Organization" onClick={() => setSelectedKey('Edit Organization')}>
            <StyledText size="xlarge">Edit Organization</StyledText>
          </Menu.Item>
          )}
        </StyledMenu>
        {content}
      </Root>
    </>
  );
};

export default Settings;
