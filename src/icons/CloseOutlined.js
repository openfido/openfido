import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';
import colors from 'styles/colors';

const CloseOutlined = ({ color, onClick }) => {
  const CloseOutlinedSVG = () => (
    <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
      <line x1="21.2929" y1="21.7071" x2="8.29289" y2="8.70711" stroke={color in colors ? colors[color] : colors.lightGray} strokeWidth="2" />
      <line x1="8.28417" y1="21.4621" x2="21.1218" y2="8.30172" stroke={color in colors ? colors[color] : colors.lightGray} strokeWidth="2" />
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
