import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';

import { inviteOrganizationMember } from 'actions/organization';
import CloseOutlined from 'icons/CloseOutlined';
import {
  StyledH2,
  StyledModal,
  StyledInput,
  StyledButton,
  StyledText,
} from 'styles/app';
import colors from 'styles/colors';

const Modal = styled(StyledModal)`
  h2 {
    text-transform: uppercase;
    color: ${colors.black};
    text-align: center;
    line-height: 32px;
    line-height: 2rem;
    margin-bottom: 32px;
  }
  .anticon {
    top: 18px;
    right: 18px;
  }
  .ant-modal-body {
    padding: 92px 45px 198px 45px;
    border-radius: 3px;
  }
  .ant-modal-content {
    box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.05);
  }
  form {
    text-align: center;
    button[type="submit"] {
      margin-top: 24px;
      margin-top: 1.5rem;
    }
  }
`;

const FormMessage = styled.div`
  padding-top: 0.25rem;
  font-size: 12px;
  line-height: 14px;
  height: 18px;
  height: 1.125rem;
`;

const InviteUserPopup = ({ handleOk, handleCancel }) => {
  const profile = useSelector((state) => state.user.profile);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const userInvited = useSelector((state) => state.organization.userInvited);
  const inviteOrganizationMemberError = useSelector((state) => state.organization.inviteOrganizationMemberError);
  const [email, setEmail] = useState(null);
  const dispatch = useDispatch();

  useEffect(() => {
    if (!inviteOrganizationMemberError && userInvited) {
      handleOk();
    }
  }, [inviteOrganizationMemberError, userInvited]);

  if (!profile || !profile.organizations || !profile.organizations.length) return null;

  const currentOrgObj = profile.organizations.find((org) => org.uuid === currentOrg);

  const onEmailChanged = (e) => {
    setEmail(e.target.value);
  };

  const onInviteClicked = (e) => {
    e.preventDefault();

    dispatch(inviteOrganizationMember(currentOrg, email));
  };

  return (
    <Modal
      visible
      footer={null}
      onOk={handleOk}
      onCancel={handleCancel}
      closeIcon={<CloseOutlined />}
      width={390}
    >
      <StyledH2>
        INVITE A USER TO JOIN
        <br />
        {currentOrgObj && currentOrgObj.name}
      </StyledH2>
      <form onSubmit={onInviteClicked}>
        <StyledInput shape="round" placeholder="email address" onChange={onEmailChanged} />
        <FormMessage>
          <StyledText color="pink">
            {inviteOrganizationMemberError && 'Invitation could not be sent.'}
          </StyledText>
        </FormMessage>
        <StyledButton
          htmlType="submit"
          color="blue"
          size="middle"
          width={108}
          onClick={onInviteClicked}
        >
          Invite
        </StyledButton>
      </form>
    </Modal>
  );
};

InviteUserPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
};

export default InviteUserPopup;
