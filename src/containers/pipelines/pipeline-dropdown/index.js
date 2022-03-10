import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

import DownOutlined from 'icons/DownOutlined';
import {
  StyledText,
} from 'styles/app';
import { Dropdown, Menu } from 'antd';
import colors from 'styles/colors';

import axios from 'axios';
import PipelineSelector from './pipeline-selector';

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
  console.log('pd', updateFromDropdown);
  const [gtoken, setToken] = useState(false);

  const [pipelines, setPipelines] = useState([
    {
      full_name: '',
      url: '',
      id: '',
    },
  ]);

  useEffect(() => {
    console.log('UE');
    axios.get('http://localhost:3005/gtoken')
      .then((response) => {
        if (response.data !== 'undefined') {
          setToken(response);
        }
      }, (error) => {
        console.log(error);
      });
  }, []);

  useEffect(() => {
    console.log('UEP');
    axios.get('http://localhost:3005/autogenPipelines')
      .then((response) => {
        console.log(response);
        if (response.data !== 'undefined') {
          setPipelines(response.data);
        }
      }, (error) => {
        console.log(error);
      });
  }, []);

  const menu = (
    <AppDropdownMenu>
      <AppDropdownMenuItem>
        {pipelines.map((pipe) => <PipelineSelector pipeline={pipe} updateFromDropdown={updateFromDropdown} />)}
      </AppDropdownMenuItem>
    </AppDropdownMenu>
  );

  /*
  if (gtoken) {
    console.log('hmm', gtoken);
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
  }
  return (
    <a className="btn" href="http://localhost:3005/auth">Enable pre-select from GITHUB</a>
  );
  */

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

/*
        <button type="button" onClick={buttonAuth()}>
          Enable pre-select from GITHUB
        </button>
        */

export default PipelineDropdown;
