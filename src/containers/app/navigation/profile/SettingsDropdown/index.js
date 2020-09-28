import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { Dropdown, Menu } from 'antd';

import { logoutUser as logoutUserAction } from 'actions/user';
import DownOutlined from 'icons/DownOutlined';

const { Item } = Menu;

const StyledMenu = styled(Menu)`
  display: block;
  min-width: auto;
  width: 118px;
  margin: 0 auto;
  background: #f7f7f7;
  padding: 18px 0;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
  box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.05);
  top: 7px;
`;

const StyledMenuItem = styled(Item)`
  text-align: center;
  font-size: 12px;
  line-height: 14px;
  font-weight: 500;
  padding: 0;
  a {
    padding: 8px 0;
    margin: 0;
  }
`;

const SettingsDropdown = ({ logoutUser }) => {
  const menu = (
    <StyledMenu>
      <StyledMenuItem>
        <Link to="/profile">Account Profile</Link>
      </StyledMenuItem>
      <StyledMenuItem>
        <Link to="/login" onClick={logoutUser}>Sign Out</Link>
      </StyledMenuItem>
    </StyledMenu>
  );

  return (
    <Dropdown overlay={menu}>
      <div>
        Manage settings
        <DownOutlined color="gray" />
      </div>
    </Dropdown>
  );
};

SettingsDropdown.propTypes = {
  logoutUser: PropTypes.func.isRequired,
};

const mapDispatch = (dispatch) => bindActionCreators({
  logoutUser: logoutUserAction,
}, dispatch);

export default connect(undefined, mapDispatch)(SettingsDropdown);
