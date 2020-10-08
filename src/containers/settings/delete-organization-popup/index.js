import React, { useState } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { Space } from 'antd';

import { requestDeleteOrganization } from 'services';
import CloseOutlined from 'icons/CloseOutlined';
import AlertOutlined from 'icons/AlertOutlined';
import CheckOutlined from 'icons/CheckOutlined';
import CheckFilled from 'icons/CheckFilled';
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
    margin-bottom: 0;
  }
  .anticon-close-outlined {
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
`;

const StyledForm = styled.div`
  text-align: center;
  input {
    width: 354px;
    margin-left: -1.125rem;
    font-weight: 900;
    font-size: 20px;
    line-height: 24px;
    line-height: 1.5rem;
    text-align: center;
  }
  button {
    filter: drop-shadow(2px 3px 4px rgba(0, 0, 0, 0.05));
    margin-bottom: -20px;
    margin-bottom: -1.25rem;
  }
`;

const ConfirmBox = styled.div`
  border-radius: 3px;
  text-align: left;
  width: 354px;
  border: 2px solid ${colors.pink};
  display: flex;
  padding: 12px 14px;
  padding: 0.75rem 0.875rem 0.75rem 0.5rem;
  cursor: pointer;
  filter: drop-shadow(2px 3px 4px rgba(0, 0, 0, 0.05));
  margin: 24px 0 32px 18px;
  margin: 1.5rem 0 2rem -1.125rem;
  user-select: none;
`;

const ConfirmCheck = styled.div`
  display: block;
  min-width: 60px;
  text-align: center;
  margin-right: 8px;
  margin-right: 0.5rem;
  line-height: 12px;
  .anticon {
    position: static;
  }
`;

const DeleteOrganizationPopup = ({
  handleOk, handleCancel, organizationUUID, organizationName,
}) => {
  const [deleteName, setDeleteName] = useState(null);
  const [goToDelete, setGoToDelete] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [loading, setLoading] = useState(false);

  const onDeleteNameChanged = (e) => {
    setDeleteName(e.target.value);
  };

  const onPermanentlyDeleteClicked = () => {
    if (deleteName === organizationName && confirmDelete && !loading) {
      setLoading(true);
      requestDeleteOrganization(organizationUUID)
        .then(() => {
          handleOk();
        })
        .catch(() => {
          setLoading(false);
        });
    }
  };

  return (
    <div role="dialog" onClick={(e) => e.stopPropagation()}>
      <Modal
        visible
        footer={null}
        onOk={handleOk}
        onCancel={handleCancel}
        closeIcon={<CloseOutlined />}
        width={390}
      >
        {goToDelete ? (
          <>
            <StyledH2 color="gray">
              <Space direction="vertical" size={16}>
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
                  <strong>{organizationName}</strong>
                  {' '}
                  to confirm
                </p>
              </Space>
            </StyledH2>
            <StyledForm onSubmit={onPermanentlyDeleteClicked}>
              <StyledInput value={deleteName} onChange={onDeleteNameChanged} />
              <ConfirmBox onClick={() => setConfirmDelete(!confirmDelete)}>
                <ConfirmCheck>
                  {confirmDelete ? <CheckFilled /> : <CheckOutlined />}
                  <StyledText size="small" color="pink">{confirmDelete ? 'confirmed' : 'confirm'}</StyledText>
                </ConfirmCheck>
                <StyledText size="large" color="pink">
                  I understand that upon deletion, this data will no longer be available.
                </StyledText>
              </ConfirmBox>
              <StyledButton size="middle" width={128} color="pink" onClick={onPermanentlyDeleteClicked}>
                <label>
                  Permanently
                  <br />
                  Delete
                </label>
              </StyledButton>
            </StyledForm>
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
    </div>
  );
};

DeleteOrganizationPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
  organizationUUID: PropTypes.string.isRequired,
  organizationName: PropTypes.string.isRequired,
};

export default DeleteOrganizationPopup;
