import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useDispatch, useSelector } from 'react-redux';
import { Dropdown, Menu } from 'antd';
import styled from 'styled-components';
import moment from 'moment';

import {
  ROLE_ADMINISTRATOR,
  ROLE_USER,
} from 'config/roles';
import { requestCancelOrganizationInvitation } from 'services';
import { getOrganizationMembers, removeOrganizationMember, changeOrganizationMemberRole } from 'actions/organization';
import DownOutlined from 'icons/DownOutlined';
import DeleteOutlined from 'icons/DeleteOutlined';
import {
  StyledGrid,
  StyledText,
} from 'styles/app';
import colors from 'styles/colors';

const UserItemGrid = styled(StyledGrid)`
  padding: 16px;
  padding: 1rem;
`;

const StyledDropdown = styled(Dropdown)`
  position: relative;
  &.ant-dropdown-trigger {
    width: 116px;
    display: inline-flex;
    justify-content: space-between;
  }
`;

const DeleteColumn = styled.div`
  position: relative;
  .anticon {
    left: 0;
    top: -10px;
    top: -0.625rem;
  }
`;

/*const ErrorMessage = styled(StyledText)`
  position: absolute;
  right: 32px;
  right: 2rem;
`;*/

const StyledMenu = styled(Menu)`
  display: block;
  width: 178px;
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

const NameColumn = styled.div`
  position: relative;
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
  &:hover, &.ant-dropdown-menu-item-selected {
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

const UserItem = ({
  uuid, first_name, last_name, is_system_admin, last_active_at, role, isInvited,
}) => {
  const [userRole, setUserRole] = useState(role || ROLE_USER);
  const [userRoleClicked, setUserRoleClicked] = useState(null);
  const [invitationCanceled, setInvitationCanceled] = useState(false);

  const currentOrg = useSelector((state) => state.user.currentOrg);
  const userRemoved = useSelector((state) => state.organization.messages.userRemoved);
  const removeMemberError = useSelector((state) => state.organization.messages.removeMemberError);
  const userRoleChanged = useSelector((state) => state.organization.messages.userRoleChanged);
  const changeRoleError = useSelector((state) => state.organization.messages.changeRoleError);
  const dispatch = useDispatch();

  useEffect(() => {
    if (!changeRoleError && userRoleChanged === uuid && userRoleClicked) {
      setUserRole(userRoleClicked);
      setUserRoleClicked(null);
    }
  }, [changeRoleError, userRoleChanged, uuid, userRoleClicked]);

  if (invitationCanceled) return null;

  const onDeleteUserClicked = () => {
    if (isInvited && uuid) {
      requestCancelOrganizationInvitation(uuid)
        .then(() => {
          dispatch(getOrganizationMembers(currentOrg));
          setInvitationCanceled(true);
        })
        .catch(() => {
          setInvitationCanceled(false);
        });
    } else {
      dispatch(removeOrganizationMember(currentOrg, uuid));
    }
  };

  const onChangeRoleClicked = (clickedRole) => {
    dispatch(changeOrganizationMemberRole(currentOrg, uuid, clickedRole.code))
      .then(() => setUserRoleClicked(clickedRole));
  };

  const menu = (
    <StyledMenu selectedKeys={[userRole && userRole.name]}>
      <li>
        <StyledText size="large" fontweight={500}>Change role</StyledText>
      </li>
      <StyledMenuItem
        key={ROLE_ADMINISTRATOR.name}
        title={ROLE_ADMINISTRATOR.name}
        onClick={() => onChangeRoleClicked(ROLE_ADMINISTRATOR)}
      >
        <span>{ROLE_ADMINISTRATOR.name}</span>
      </StyledMenuItem>
      <li>
        Able to manage
        {' '}
        <strong>Users</strong>
        ,
        {' '}
        <strong>Pipelines</strong>
        ,
        {' '}
        <strong>Files</strong>
        {' '}
        for this organization.
      </li>
      <StyledMenuItem
        key={ROLE_USER.name}
        title={ROLE_USER.name}
        onClick={() => onChangeRoleClicked(ROLE_USER)}
      >
        <span>{ROLE_USER.name}</span>
      </StyledMenuItem>
      <li>
        Able to manage
        {' '}
        <strong>Pipelines</strong>
        {' '}
        and
        {' '}
        <strong>Files</strong>
        {' '}
        for this organization.
      </li>
    </StyledMenu>
  );

  const roleText = (
    <StyledText size="large" color="gray">
      {userRole && userRole.name}
      {!isInvited && <DownOutlined color="lightGray" />}
    </StyledText>
  );

  return (
    <UserItemGrid gridTemplateColumns="3fr 2fr 2fr minmax(208px, 1fr)" bgcolor="white">
      <NameColumn>
        <StyledText size="large" color="gray">
          {first_name}
          {last_name && ` ${last_name}`}
        </StyledText>
        {/*{removeMemberError && uuid === userRemoved && (
          <ErrorMessage color="pink">This user could not be deleted.</ErrorMessage>
        )}
        {changeRoleError && uuid === userRoleChanged && (
          <ErrorMessage color="pink">Cannot change this member's role.</ErrorMessage>
        )}*/}
      </NameColumn>
      {isInvited ? roleText : (
          <StyledDropdown overlay={menu} trigger="click">
            {roleText}
          </StyledDropdown>
      )}
      <StyledText size="large" color="gray">
        {isInvited ? (
          <StyledText color="blue">Invitation sent</StyledText>
        ) : (
          moment.utc(last_active_at).fromNow()
        )}
      </StyledText>
      <DeleteColumn>
        <DeleteOutlined color="gray20" onClick={onDeleteUserClicked} />
      </DeleteColumn>
    </UserItemGrid>
  );
};

UserItem.propTypes = {
  uuid: PropTypes.string,
  first_name: PropTypes.string.isRequired,
  last_name: PropTypes.string,
  is_system_admin: PropTypes.bool,
  last_active_at: PropTypes.string,
  role: PropTypes.shape({
    uuid: PropTypes.string,
    name: PropTypes.string.isRequired,
    code: PropTypes.string.isRequired,
  }).isRequired,
  isInvited: PropTypes.bool,
};

UserItem.defaultProps = {
  uuid: null,
  last_name: '',
  is_system_admin: false,
  last_active_at: undefined,
  isInvited: false,
};

export default UserItem;
