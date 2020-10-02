import React from 'react';
import styled from 'styled-components';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';

import { logoutUser } from 'actions/user';
import colors from 'styles/colors';

import SettingsDropdown from './SettingsDropdown';
import PhotoImg from './images/navigation-profile-avatar.svg';

const StyledProfileContainer = styled.div`
  position: relative;
  text-align: center;
  cursor: pointer;
  border-bottom: 1px solid #d2d2d2;
  margin: 32px 20px 0 16px;
  font-size: 14px;
  line-height: 14px;
`;

const StyledPhotoContainer = styled.div`
  width: 46px;
  height: 46px;
  border-radius: 22px;
  border: 2px solid ${colors.black};
  padding: 1px;
  margin: -2px auto;
`;

const StyledPhoto = styled.div`
  width: 40px;
  height: 40px;
  background-image: url(${PhotoImg});
  background-size: 40px;
  border-radius: 20px;
`;

const StyledName = styled.div`
  font-size: 18px;
  font-weight: 500;
  line-height: 21px;
  margin: 8px auto 12px auto;
`;

const SignOutLink = styled.div`
  position: absolute;
  right: 20px;
  right: 1.25rem;
  top: 8px;
  top: 0.5rem;
`;

const Profile = () => {
  const profile = useSelector((state) => state.user.profile);
  const dispatch = useDispatch();

  if (!profile) return null;

  const onSignOutClicked = () => {
    dispatch(logoutUser());
  };

  return (
    <>
      <SignOutLink>
        <Link to="/login" onClick={onSignOutClicked}>Sign Out</Link>
      </SignOutLink>
      <StyledProfileContainer>
        <StyledPhotoContainer>
          <StyledPhoto />
        </StyledPhotoContainer>
        <StyledName>
          {profile.first_name}
          {profile.last_name && ` ${profile.last_name}`}
        </StyledName>
        <SettingsDropdown />
      </StyledProfileContainer>
    </>
  );
};

export default Profile;
