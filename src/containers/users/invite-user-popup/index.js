import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';

import { getOrganizationMembers, inviteOrganizationMember } from 'actions/organization';
import {
  StyledH2, StyledModal, StyledInput, StyledButton,
} from 'styles/app';
import colors from 'styles/colors';

const Modal = styled(StyledModal)`
  h2 {
    text-transform: uppercase;
    color: ${colors.black};
    text-align: center;
    line-height: 32px;
    line-height: 2rem;
  }
  .ant-modal-body {
    padding: 92px 45px 198px 45px;
  }
  input {
    margin: 42px auto;
  }
  form {
    text-align: center;
  }
`;


const InviteUserPopup = ({ handleOk, handleCancel }) => {
  const profile = useSelector((state) => state.user.profile);
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const [email, setEmail] = useState(null);
  const dispatch = useDispatch();

  useEffect(() => { // TODO
    if (profile) {
      dispatch(getOrganizationMembers(currentOrg));
    }
  }, [getOrganizationMembers, profile, currentOrg]);

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
      width={390}
    >
      <StyledH2>
        INVITE A USER TO JOIN
        <br />
        {currentOrgObj && currentOrgObj.name}
      </StyledH2>
      <form onSubmit={onInviteClicked}>
        <StyledInput shape="round" placeholder="email address" onChange={onEmailChanged} />
        <StyledButton
          type="submit"
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
