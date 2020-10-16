import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';
import { Dropdown, Menu } from 'antd';

import { changeOrganization } from 'actions/user';
import DownOutlined from 'icons/DownOutlined';
import colors from 'styles/colors';

const StyledDropdown = styled(Dropdown)`
  position: relative;
  padding-bottom: 16px;
  padding-bottom: 1rem;
  .anticon {
    position: absolute;
    top: 4px;
    top: 0.25rem;
  }
`;

const StyledMenu = styled(Menu)`
  display: block;
  margin: 0 auto;
  top: -4px;
  width: 191px;
  background: ${colors.white};
  padding: 4px 32px 24px 32px;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
  box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.03);
  border: 0.5px solid ${colors.lightGray};
  font-weight: 500;
  color: ${colors.gray};
  li:first-child {
    font-size: 12px;
    line-height: 14px;
    margin-top: 4px;
    margin-top: 0.25rem;
    margin-bottom: 16px;
    margin-bottom: 1rem;
    text-align: center;
  }
`;

const StyledMenuItem = styled(Menu.Item)`
  color: ${colors.gray};
  font-size: 14px;
  line-height: 16px;
  font-weight: 500;
  border: 1px solid ${colors.lightBorder};
  border-radius: 3px;
  padding: 2px;
  &:hover {
    background-color: ${colors.blue};
    border-color: transparent;
    color: ${colors.white};
  }
  &:not(:last-child) {
    margin-bottom: 10px;
    margin-bottom: 0.625rem;
   }
`;

const SettingsDropdown = () => {
  const organizations = useSelector((state) => state.user.organizations);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const dispatch = useDispatch();

  const onOrgClicked = (organization_uuid) => {
    dispatch(changeOrganization(organization_uuid));
  };

  const menu = (
    <StyledMenu>
      <li>Change organization</li>
      {organizations && organizations.map((org) => (
        <StyledMenuItem key={org.uuid} onClick={() => onOrgClicked(org.uuid)}>
          {org.name}
        </StyledMenuItem>
      ))}
    </StyledMenu>
  );

  const currentOrgObj = organizations && organizations.find((org) => org.uuid === currentOrg);
  const dropdownDisabled = currentOrgObj && organizations && organizations.length <= 1;

  return (
    <>
      {organizations && !!organizations.length && (
        <StyledDropdown overlay={menu} disabled={dropdownDisabled}>
          <div>
            <span>
              {currentOrgObj ? currentOrgObj.name : 'No organization'}
              {!dropdownDisabled && <DownOutlined color="lightGray" />}
            </span>
          </div>
        </StyledDropdown>
      )}
    </>
  );
};

export default SettingsDropdown;
