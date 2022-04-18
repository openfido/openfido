import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

import DownOutlined from 'icons/DownOutlined';
import {
  StyledText,
} from 'styles/app';
import { Dropdown, Menu } from 'antd';

import colors from 'styles/colors';

import gitApi from 'util/api-github';
import PipelineSelector from './pipeline-selector';

const AppDropdown = styled(Dropdown)`
  float: left;
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
  margin-bottom: 70px;
  margin-left: 15px;
  height: auto;
`;

const AppDropdownMenuItem = styled(Menu.Item)`
  padding: 10px;
  padding: 0.625rem;
  text-align: left;
  height: auto;
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
  const [pipelines, setPipelines] = useState([
    {
      full_name: '',
      url: '',
      id: '',
      description: '',
    },
  ]);

  useEffect(() => {
    gitApi.getPotentialPipelines()
      .then((response) => {
        if (response !== 'undefined') {
          setPipelines(response);
        }
      }, (error) => {
        console.log(error);
      });
  }, []);

  const menu = (
    <AppDropdownMenu>
      <AppDropdownMenuItem>
        {pipelines.map((pipe) => (
          <PipelineSelector
            pipeline={pipe}
            key={pipe.id}
            updateFromDropdown={updateFromDropdown}
          />
        ))}
      </AppDropdownMenuItem>
    </AppDropdownMenu>
  );

  return (
    <AppDropdown overlay={menu} trigger="click">
      <div aria-label="App dropdown">
        <StyledText style={{ textAlign: 'left' }} color="darkText">
          Import from Github
        </StyledText>
        <DownOutlined color="gray20" />
      </div>
    </AppDropdown>
  );
};

export default PipelineDropdown;
