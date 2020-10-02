import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { Space } from 'antd';

import { requestOrganizationMembers } from 'services';
import {
  StyledTitle, StyledButton, StyledGrid, StyledText,
} from 'styles/app';
import UserItem from './user-item';

function Users() {
  const profile = useSelector((state) => state.user.profile);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (profile && currentOrg) {
        requestOrganizationMembers(currentOrg, profile.token)
            .then((response) => setUsers(response.data))
            .catch((response) => setError(true));
    }
  }, [requestOrganizationMembers, profile, currentOrg]);

  if (!profile) return null;

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
      <StyledGrid gridTemplateColumns="3fr 2fr 2fr 1fr">
        <StyledText size="large" fontweight={500} color="black">Name</StyledText>
        <StyledText size="large" fontweight={500} color="black">Role</StyledText>
        <StyledText size="large" fontweight={500} color="black">Last Activity</StyledText>
      </StyledGrid>
      <Space direction="vertical" size={16}>
        {users.map((item) => (
          <UserItem key={item.uuid} {...item} />
        ))}
      </Space>
    </>
  );
}


export default Users;
