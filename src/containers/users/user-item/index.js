import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useDispatch, useSelector } from 'react-redux';
import { Dropdown, Menu } from 'antd';
import styled from 'styled-components';
import moment from 'moment';

import { removeOrganizationMember, changeOrganizationMemberRole } from 'actions/organization';
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
    width: 116px;
    display: inline-flex;
    justify-content: space-between;
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

const ErrorMessage = styled(StyledText)`
  position: absolute;
  right: 32px;
  right: 2rem;
`;

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

const User = ({
  uuid: user_uuid, first_name, last_name, is_system_admin, last_active_at, role,
}) => {
  const [userRole, setUserRole] = useState(role.name);
  const [userRoleClicked, setUserRoleClicked] = useState();
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const userRemoved = useSelector((state) => state.organization.userRemoved);
  const removeMemberError = useSelector((state) => state.organization.removeMemberError);
  const userRoleChanged = useSelector((state) => state.organization.userRoleChanged);
  const changeRoleError = useSelector((state) => state.organization.changeRoleError);
  const dispatch = useDispatch();

  useEffect(() => {
    if (!changeRoleError && userRoleChanged === user_uuid) {
      setUserRole(userRoleClicked);
    }
  }, [changeRoleError, userRoleChanged, user_uuid, userRoleClicked]);

  const onDeleteUserClicked = () => {
    dispatch(removeOrganizationMember(currentOrg, user_uuid));
  };

  const onChangeRoleClicked = (clickedRole) => {
    dispatch(changeOrganizationMemberRole(currentOrg, user_uuid, clickedRole))
      .then(() => setUserRoleClicked(clickedRole));
  };

  const menu = (
    <StyledMenu selectedKeys={[userRole]}>
      <li>
        <StyledText size="large" fontweight={500}>Change role</StyledText>
      </li>
      <StyledMenuItem
        key="Administrator"
        onClick={() => onChangeRoleClicked('Administrator')}
      >
        <span>Administrator</span>
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
        key="Engineer"
        onClick={() => onChangeRoleClicked('Engineer')}
      >
        <span>Engineer</span>
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
      <StyledMenuItem
        key="Unassigned"
        onClick={() => onChangeRoleClicked('Unassigned')}
      >
        <span>Unassigned</span>
      </StyledMenuItem>
      <li>View only.</li>
    </StyledMenu>
  );

  return (
    <StyledGrid gridTemplateColumns="3fr 2fr 2fr minmax(208px, 1fr)" bgcolor="white">
      <NameColumn>
        <StyledText size="large" color="gray">
          {first_name}
          {last_name && ` ${last_name}`}
        </StyledText>
        {removeMemberError && user_uuid === userRemoved && (
          <ErrorMessage color="pink">This user could not be deleted.</ErrorMessage>
        )}
        {changeRoleError && user_uuid === userRoleChanged && (
          <ErrorMessage color="pink">Cannot change this member's role.</ErrorMessage>
        )}
      </NameColumn>
      <StyledDropdown overlay={menu} trigger="click">
        <StyledText size="large" color="gray">
          {changeRoleError && user_uuid === userRoleChanged ? role.name : userRole}
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

User.propTypes = {
  uuid: PropTypes.string.isRequired,
  first_name: PropTypes.string.isRequired,
  last_name: PropTypes.string.isRequired,
  is_system_admin: PropTypes.bool.isRequired,
  last_active_at: PropTypes.string.isRequired,
  role: PropTypes.shape({
    uuid: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    code: PropTypes.string.isRequired,
  }),
};

User.defaultProps = {
  role: {},
};

export default User;
