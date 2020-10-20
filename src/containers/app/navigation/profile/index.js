import React from 'react';
import styled from 'styled-components';
import { useSelector } from 'react-redux';
import colors from 'styles/colors';
import PhotoImg from 'icons/navigation-profile-avatar.svg';
import SettingsDropdown from './SettingsDropdown';

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

const StyledName = styled.div`
  font-size: 18px;
  font-weight: 500;
  line-height: 21px;
  margin: 8px auto 12px auto;
`;

const Profile = () => {
  const profile = useSelector((state) => state.user.profile);
  const avatar = useSelector((state) => state.user.avatar);

  const StyledPhoto = styled.div`
    width: 40px;
    height: 40px;
    background-image: url(${avatar || PhotoImg});
    background-size: 40px;
    border-radius: 20px;
  `;

  return (
    <>
      <StyledProfileContainer>
        <StyledPhotoContainer>
          <StyledPhoto />
        </StyledPhotoContainer>
        {profile && (
          <StyledName>
            {profile.first_name}
            {profile.last_name && ` ${profile.last_name}`}
          </StyledName>
        )}
        <SettingsDropdown />
      </StyledProfileContainer>
    </>
  );
};

export default Profile;
