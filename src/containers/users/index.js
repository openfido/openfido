import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useDispatch, useSelector } from 'react-redux';
import { Space } from 'antd';

import { ROLE_UNASSIGNED } from 'config/roles';
import { getOrganizationMembers } from 'actions/organization';
import {
  StyledTitle,
  StyledButton,
  StyledGrid,
  StyledText,
} from 'styles/app';
import UserItem from './user-item';
import InviteUserPopup from './invite-user-popup';

const HeaderRow = styled(StyledGrid)`
  padding: 12px 16px 20px 16px;
  padding: 0.75rem 1rem 1.25rem; 1rem;
`;

const Users = () => {
  const [showInviteUserPopup, setShowInviteUserPopup] = useState(false);

  const profile = useSelector((state) => state.user.profile);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const members = useSelector((state) => state.organization.members);
  const invitations = useSelector((state) => state.organization.invitations);
  const dispatch = useDispatch();

  useEffect(() => {
    if (profile && currentOrg) {
      dispatch(getOrganizationMembers(currentOrg));
    }
  }, [dispatch, profile, currentOrg]);

  const openInviteUserPopup = () => setShowInviteUserPopup(true);

  const closeInviteUserPopup = () => {
    dispatch(getOrganizationMembers(currentOrg));
    setShowInviteUserPopup(false);
  };

  return (
    <>
      <StyledTitle>
        <div>
          <h1>Users</h1>
          <StyledButton onClick={openInviteUserPopup} size="small">
            + Invite User
          </StyledButton>
        </div>
      </StyledTitle>
      <HeaderRow gridTemplateColumns="3fr 2fr 2fr minmax(208px, 1fr)">
        <StyledText size="large" fontweight={500} color="black">Name</StyledText>
        <StyledText size="large" fontweight={500} color="black">Role</StyledText>
        <StyledText size="large" fontweight={500} color="black">Last Activity</StyledText>
      </HeaderRow>
      <Space direction="vertical" size={16}>
        {members && members.map(({
          uuid: user_uuid, first_name, last_name, role, is_system_admin, last_active_at,
        }) => (
          <UserItem
            key={`${user_uuid}${role && role.code}`}
            uuid={user_uuid}
            first_name={first_name}
            last_name={last_name}
            role={role}
            is_system_admin={is_system_admin}
            last_active_at={last_active_at}
          />
        ))}
        {invitations && invitations.map(({ uuid: invitation_uuid, email_address }) => (
          <UserItem
            key={invitation_uuid}
            uuid={invitation_uuid}
            role={ROLE_UNASSIGNED}
            first_name={email_address}
            isInvited
          />
        ))}
      </Space>
      {showInviteUserPopup && (
        <InviteUserPopup
          handleOk={closeInviteUserPopup}
          handleCancel={closeInviteUserPopup}
        />
      )}
    </>
  );
};

export default Users;
