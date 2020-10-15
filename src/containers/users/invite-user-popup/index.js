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
  .anticon-close-outlined {
    top: 18px;
    right: 18px;
  }
  .ant-modal-body {
    padding: 92px 45px 198px 45px;
    border-radius: 3px;
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
  padding-top: 0.5rem;
  font-size: 12px;
  line-height: 14px;
  height: 16px;
  height: 1rem;
`;

const InviteUserPopup = ({ handleOk, handleCancel }) => {
  const organizations = useSelector((state) => state.user.organizations);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const userInvited = useSelector((state) => state.organization.messages.userInvited);
  const inviteOrganizationMemberError = useSelector((state) => state.organization.messages.inviteOrganizationMemberError);
  const [email, setEmail] = useState(null);
  const dispatch = useDispatch();

  useEffect(() => {
    if (!inviteOrganizationMemberError && userInvited) {
      handleOk();
    }
  }, [inviteOrganizationMemberError, userInvited, handleOk]);

  const currentOrgObj = currentOrg && organizations && organizations.find((org) => org.uuid === currentOrg);

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
      mask={false}
      onOk={handleOk}
      onCancel={handleCancel}
      closeIcon={<CloseOutlined />}
      width={390}
      style={{ top: '92px' }}
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
          size="middle"
          color="blue"
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
