import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';
import colors from 'styles/colors';

const MenuOutlined = (props) => {
  const { color } = props;

  const color1 = color in colors ? colors[color] : colors.white;

  const MenuOutlinedSVG = () => (
    <svg width="28" height="18" viewBox="0 0 28 18" fill="none" xmlns="http://www.w3.org/2000/svg">
      <line y1="1" x2="28" y2="1" stroke={color1} strokeWidth="2" strokeLinejoin="round" />
      <line y1="9" x2="28" y2="9" stroke={color1} strokeWidth="2" strokeLinejoin="round" />
      <line y1="17" x2="28" y2="17" stroke={color1} strokeWidth="2" strokeLinejoin="round" />
    </svg>
  );

  const color2 = color in colors ? colors[color] : colors.darkGray;

  const MenuOutlinedDarkSVG = () => (
    <svg width="12" height="15" viewBox="0 0 12 15" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 1H12" stroke={color2} strokeWidth="2" strokeLinejoin="round" />
      <line y1="7.35486" x2="12" y2="7.35486" stroke={color2} strokeWidth="2" strokeLinejoin="round" />
      <line y1="13.7097" x2="12" y2="13.7097" stroke={color2} strokeWidth="2" strokeLinejoin="round" />
    </svg>
  );

  return (
    <StyledIcon component={color === 'darkGray' ? MenuOutlinedDarkSVG : MenuOutlinedSVG} />
  );
};

MenuOutlined.propTypes = {
  color: PropTypes.string,
};

MenuOutlined.defaultProps = {
  color: colors.darkGray,
};

export default MenuOutlined;
