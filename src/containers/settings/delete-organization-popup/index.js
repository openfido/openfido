import React, { useState } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { Space } from 'antd';

import { requestDeleteOrganization } from 'services';
import CloseOutlined from 'icons/CloseOutlined';
import AlertOutlined from 'icons/AlertOutlined';
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
    line-height: 48px;
    line-height: 3rem;
    margin-bottom: 32px;
    position: relative;
    .anticon {
      right: auto;
      top: 16px;
      top: 1rem;
      margin-left: 8px;
      margin-left: 0.5rem;
    }
    p {
      text-align: center;
      line-height: 32px;
      line-height: 2rem;
    }
  }
  .anticon {
    top: 18px;
    right: 18px;
  }
  .ant-modal-body {
    padding: 24px 48px 48px 36px;
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

const DeleteOrganizationPopup = ({
  handleOk, handleCancel, organizationUUID, organizationName,
}) => {
  const [deleteName, setDeleteName] = useState(null);
  const [goToDelete, setGoToDelete] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  const onDeleteNameChanged = (e) => {
    setDeleteName(e.target.value);
  };

  const onPermanentlyDeleteClicked = () => {
    if (deleteName === organizationName && !loading) {
      setLoading(true);
      requestDeleteOrganization(organizationUUID)
        .then(() => {
          handleOk();
        })
        .catch(() => {
          setError(true);
          setLoading(false);
        });
    } else {
      setError(true);
    }
  };

  return (
    <Modal
      visible
      footer={null}
      onOk={handleOk}
      onCancel={handleCancel}
      closeIcon={<CloseOutlined />}
      width={390}
      onClick={(e) => e.stopPropagation()}
    >
      {goToDelete ? (
        <>
          <StyledH2 color="gray">
              <Space direction="vertical">
            <StyledText color="pink">
              ALERT
              <AlertOutlined />
            </StyledText>
            <p>
              You are about to delete
              {' '}
              <br />
              <StyledText color="pink">{organizationName}</StyledText>
            </p>
            <p>
              Please type in the organization
              {' '}
              {organizationName}
              {' '}
              to confirm
            </p>
              </Space>
          </StyledH2>

          <StyledButton width={128} color="pink" onClick={onPermanentlyDeleteClicked}>
            Permanently Delete
          </StyledButton>
        </>
      ) : (
        <>
          <StyledH2 color="pink">
            <StyledText color="pink">
              ALERT
              <AlertOutlined />
            </StyledText>
            <br />
            PLEASE READ FIRST.
          </StyledH2>
          <Space direction="vertical" size={36} align="center">
            <StyledText color="gray" size="large">
              Are you sure you want to delete this organization?
              {' '}
              <strong>This action cannot be undone.</strong>
              {' '}
              Please be certain.
            </StyledText>
            <StyledButton
              size="middle"
              color="blue"
              width={108}
              onClick={handleCancel}
            >
              <label>
                DO NOT
                <br />
                DELETE
              </label>
            </StyledButton>
            <StyledButton type="text" color="transparent">
              <StyledText
                size="large"
                fontweight={500}
                align="center"
                display="block"
                color="pink"
                onClick={() => setGoToDelete(true)}
              >
                Yes, I am certain that
                <br />
                I want to delete
              </StyledText>
            </StyledButton>
          </Space>
        </>
      )}
    </Modal>
  );
};

DeleteOrganizationPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
};

export default DeleteOrganizationPopup;

/*
<form onSubmit={onInviteClicked}>
<StyledInput shape="round" placeholder="email address" onChange={onEmailChanged} />
<FormMessage>
<StyledText color="pink">
{inviteOrganizationMemberError && 'Invitation could not be sent.'}
</StyledText>
</FormMessage> */
