import React from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { Dropdown, Menu } from 'antd';

import { ROUTE_LOGOUT } from 'config/routes';
import {
  StyledLayout,
  StyledSider,
  StyledContent,
  StyledText,
} from 'styles/app';
import colors from 'styles/colors';
import DownOutlined from 'icons/DownOutlined';
import Navigation from './navigation';

const AppDropdown = styled(Dropdown)`
  position: absolute;
  top: 24px;
  top: 1.5rem;
  right: 16px;
  right: 1rem;
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
  border: 1px solid;
  box-shadow: 2px 1px 1px black;
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

const App = ({ children }) => {
  const menu = (
    <AppDropdownMenu>
      <AppDropdownMenuItem>
        <Link
          aria-label="Log Out link"
          to={ROUTE_LOGOUT}
        >
          Log Out
        </Link>
      </AppDropdownMenuItem>
    </AppDropdownMenu>
  );

  return (
    <StyledLayout>
      <StyledSider width={250} theme="light">
        <Navigation />
      </StyledSider>
      <StyledContent>
        <AppDropdown overlay={menu} trigger="click">
          <div aria-label="App dropdown">
            <StyledText color="darkText">
              OpenFIDO
            </StyledText>
            <DownOutlined color="gray20" />
          </div>
        </AppDropdown>
        {children}
      </StyledContent>
    </StyledLayout>
  );
};

App.propTypes = {
  children: PropTypes.node,
};

App.defaultProps = {
  children: null,
};

export default App;
