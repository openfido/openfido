import React, { useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Space } from 'antd';

import { getOrganizationMembers } from 'actions/organization';
import {
  StyledTitle,
  StyledButton,
  StyledGrid,
  StyledText,
} from 'styles/app';
import UserItem from './user-item';

const Users = () => {
  const profile = useSelector((state) => state.user.profile);
  const members = useSelector((state) => state.organization.members);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const dispatch = useDispatch();

  useEffect(() => {
    if (profile && currentOrg) {
      dispatch(getOrganizationMembers(currentOrg));
    }
  }, [dispatch, profile, currentOrg]);

  return (
    <>
      <StyledTitle>
        <div>
          <h1>Users</h1>
          <StyledButton size="small">
            + Invite User
          </StyledButton>
        </div>
      </StyledTitle>
      <StyledGrid gridTemplateColumns="3fr 2fr 2fr minmax(208px, 1fr)">
        <StyledText size="large" fontweight={500} color="black">Name</StyledText>
        <StyledText size="large" fontweight={500} color="black">Role</StyledText>
        <StyledText size="large" fontweight={500} color="black">Last Activity</StyledText>
      </StyledGrid>
      <Space direction="vertical" size={16}>
        {members && members.map((item) => (
          <UserItem
            key={item.uuid}
            uuid={item.uuid}
            first_name={item.first_name}
            last_name={item.last_name}
            role={item.role}
            is_system_admin={item.is_system_admin}
            last_active_at={item.last_active_at}
          />
        ))}
      </Space>
    </>
  );
};

export default Users;
