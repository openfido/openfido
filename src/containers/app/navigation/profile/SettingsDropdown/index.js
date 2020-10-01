import React from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { Dropdown, Menu } from 'antd';

import { logoutUser } from 'actions/user';
import DownOutlined from 'icons/DownOutlined';
import colors from 'styles/colors';

const { Item } = Menu;

const StyledDropdown = styled(Dropdown)`
  background-color: ${colors.white};
  position: relative;
  display: flex;
  margin-top: 12px;
  justify-content: center;
  align-items: center;
  color: ${colors.black};
  .anticon {
    position: absolute;
    top: 4px;
    top: 0.25rem;
  }
`;

const StyledMenu = styled(Menu)`
  display: block;
  min-width: auto;
  width: 191px;
  margin: 0 auto;
  background: ${colors.white};
  padding: 4px 32px 24px 32px;
  padding: 0.25rem 2rem 1.5rem 2rem;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
  box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.03);
  border: 0.5px solid ${colors.lightGray};
  top: 12px;
  text-align: center;
  font-weight: 500;
  color: ${colors.gray};
  span {
    font-size: 12px;
    line-height: 14px;
  }
`;

const StyledMenuItem = styled(Item)`
  text-align: center;
  font-size: 14px;
  line-height: 16px;
  font-weight: 500;
  border: 1px solid ${colors.lightBorder};
  border-radius: 3px;
  padding: 2px;
  text-align: left;
  &:hover {
    background-color: ${colors.blue};
    border-color: transparent;
    a {
      color: ${colors.white};
    }
  }
  a {
    color: ${colors.gray};
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

const SettingsDropdown = () => {
  const profile = useSelector((state) => state.user.profile);
  const dispatch = useDispatch();

  const onSignOutClicked = () => {
    dispatch(logoutUser());
  };

  const menu = (
    <StyledMenu>
      <span>Change organization</span>
      <StyledMenuItem>
        <Link to="/profile">Account Profile</Link>
      </StyledMenuItem>
      <StyledMenuItem>
        <Link to="/login" onClick={onSignOutClicked}>Sign Out</Link>
      </StyledMenuItem>
    </StyledMenu>
  );

  return (
    <StyledDropdown overlay={menu}>
      <div>
        <span>
          SLAC
          <DownOutlined color="lightGray" />
        </span>
      </div>
    </StyledDropdown>
  );
};

export default SettingsDropdown;
