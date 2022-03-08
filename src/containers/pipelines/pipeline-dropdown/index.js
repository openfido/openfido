import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import styled from 'styled-components';

import DownOutlined from 'icons/DownOutlined';
import {
  StyledLayout,
  StyledSider,
  StyledContent,
  StyledText,
} from 'styles/app';
import { Dropdown, Menu } from 'antd';
import colors from 'styles/colors';

import { ROUTE_LOGOUT } from 'config/routes';

const AppDropdown = styled(Dropdown)`
  user-select: none;
  z-index: 3;
  .anticon {
    border-radius: 50%;
    height: 14px;
    width: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    svg {
      width: 10px;
      height: 6px;
    }
  }
  &:hover .anticon {
    background-color: ${colors.lightGrey};
  }
`;

const AppDropdownMenu = styled(Menu)`
  filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.05));
  box-shadow: none;
  border-radius: 3px;
  padding: 0;
  min-width: 87px;
  right: 16px;
  right: 1rem;
`;

const AppDropdownMenuItem = styled(Menu.Item)`
  padding: 10px;
  padding: 0.625rem;
  text-align: center;
  a {
    color: ${colors.lightBlue};
    font-weight: 500;
    &:hover {
      color: ${colors.blue};
    }
  }
  &:hover {
    background-color: transparent;
  }
`;

const PipelineDropdown = (updateFromDropdown) => {
  // magic happens here
  const menu = (
    <AppDropdownMenu>
      <AppDropdownMenuItem>
        <Link
          aria-label="This is a test"
          to={ROUTE_LOGOUT}
        >
          This is a Test of the Emergency Dropdown System...
        </Link>
      </AppDropdownMenuItem>
    </AppDropdownMenu>
  );

  return (
    <AppDropdown overlay={menu} trigger="click">
      <div aria-label="App dropdown">
        <StyledText color="darkText">
          Import from Github
        </StyledText>
        <DownOutlined color="gray20" />
      </div>
    </AppDropdown>
  );
};

export default PipelineDropdown;
