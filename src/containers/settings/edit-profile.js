import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Space } from 'antd';
import styled from 'styled-components';

import { updateUserProfile, updateUserAvatar } from 'actions/user';
import { StyledText, StyledInput, StyledButton } from 'styles/app';
import colors from 'styles/colors';
import PhotoImg from 'icons/navigation-profile-avatar.svg';

const StyledForm = styled.form`
  display: grid;
  grid-gap: 16px;
  grid-gap: 1rem;
  max-width: 432px;
  button[type="submit"] {
    margin-top: 32px;
    margin-top: 2rem;
  }
`;

const StyledPhotoContainer = styled.div`
  width: 126px;
  height: 126px;
  border-radius: 60px;
  border: 2px solid ${colors.black};
  padding: 1px;
  margin: -2px 16px -2px 0;
  margin: -2px 1rem -2px 0;
`;

const StyledPhoto = styled.div`
  width: 120px;
  height: 120px;
  background-image: url(${PhotoImg});
  background-size: 120px;
  border-radius: 60px;
`;

const UserAvatar = styled.div`
  display: flex;
  align-items: center;
  width: 250px;
  input[type="file"] {
    display: none;
  }
`;

const FormMessage = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 32px;
  margin-top: 2rem;
`;

const EditProfile = () => {
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');

  const profile = useSelector((state) => state.user.profile);
  const avatar = useSelector((state) => state.user.avatar);
  const updateUserProfileSuccess = useSelector((state) => state.user.messages.updateUserProfileSuccess);
  const updateUserProfileInProgress = useSelector((state) => state.user.messages.updateUserProfileInProgress);
  const updateUserProfileError = useSelector((state) => state.user.messages.updateUserProfileError);
  const dispatch = useDispatch();

  useEffect(() => {
    if (profile) {
      if (profile.email) setEmail(profile.email);
      if (profile.first_name) setFirstName(profile.first_name);
      if (profile.last_name) setLastName(profile.last_name);
    }
  }, [profile]);

  if (!profile) return null;

  const onUpdateProfileClicked = (e) => {
    e.preventDefault();

    if (!updateUserProfileInProgress) {
      dispatch(updateUserProfile(profile.uuid, email, firstName, lastName));
    }
  };

  const onEmailChanged = (e) => {
    setEmail(e.target.value);
  };

  const onFirstNameChanged = (e) => {
    setFirstName(e.target.value);
  };

  const onLastNameChanged = (e) => {
    setLastName(e.target.value);
  };

  const onPhotoChanged = (e) => {
    const { files = [] } = e.target;

    if (files.length) {
      dispatch(updateUserAvatar(profile.uuid, files[0]));
      e.target.value = '';
    }
  };

  return (
    <StyledForm>
      <UserAvatar>
        <StyledPhotoContainer>
          <StyledPhoto style={avatar ? { backgroundImage: `url(${avatar}` } : null} />
        </StyledPhotoContainer>
        <input
          type="file"
          id="avatar"
          name="avatar"
          accept="image/png, image/jpeg, image/gif"
          onChange={onPhotoChanged}
        />
        <StyledButton
          htmlType="button"
          color="gray80"
          hoverbgcolor="gray"
        >
          <label htmlFor="avatar">
            Change Photo
          </label>
        </StyledButton>
      </UserAvatar>
      <div />
      <label htmlFor="first_name">
        <StyledText display="block" color="darkText">First Name</StyledText>
        <StyledInput
          type="text"
          bgcolor="white"
          size="large"
          name="first_name"
          id="first_name"
          value={firstName}
          onChange={onFirstNameChanged}
        />
      </label>
      <label htmlFor="last_name">
        <StyledText display="block" color="darkText">Last Name</StyledText>
        <StyledInput
          type="text"
          bgcolor="white"
          size="large"
          name="last_name"
          id="last_name"
          value={lastName}
          onChange={onLastNameChanged}
        />
      </label>
      <label htmlFor="email">
        <StyledText display="block" color="darkText">Email</StyledText>
        <StyledInput
          type="text"
          bgcolor="white"
          size="large"
          name="email"
          id="email"
          value={email}
          onChange={onEmailChanged}
        />
      </label>
      <Space direction="horizontal" size={24}>
        <StyledButton
          htmlType="submit"
          size="middle"
          color="blue"
          width={128}
          role="button"
          tabIndex={0}
          onClick={onUpdateProfileClicked}
        >
          Update Profile
        </StyledButton>
        <FormMessage>
          {updateUserProfileSuccess && !updateUserProfileError && <StyledText size="middle" color="green">Profile updated.</StyledText>}
          {updateUserProfileError && <StyledText size="middle" color="pink">Profile could not be updated.</StyledText>}
        </FormMessage>
      </Space>
    </StyledForm>
  );
};

export default EditProfile;
