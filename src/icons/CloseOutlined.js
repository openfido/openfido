import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';
import colors from 'styles/colors';

const CloseOutlined = ({ color, onClick }) => {
  const CloseOutlinedSVG = () => (
    <svg width="16" height="15" viewBox="8 11 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M10 12L18 20" stroke={color in colors ? colors[color] : colors.lightGray} />
      <path d="M18 12L10 20" stroke={color in colors ? colors[color] : colors.lightGray} />
    </svg>

  );

  return (
    <StyledIcon component={CloseOutlinedSVG} onClick={onClick} />
  );
};

CloseOutlined.propTypes = {
  color: PropTypes.string,
  onClick: PropTypes.func,
};

CloseOutlined.defaultProps = {
  color: colors.white,
  onClick: null,
};

export default CloseOutlined;
