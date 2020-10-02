import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';
import colors from 'styles/colors';

const DeleteOutlined = ({ color, onClick }) => {
  const DeleteOutlinedSVG = () => (
    <svg width="27" height="27" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M18.813 4.125L17.688 3h-5.625l-1.126 1.125H7v2.25h15.75v-2.25h-3.938zM8 20.714C8 21.971 9.05 23 10.333 23h9.334C20.95 23 22 21.971 22 20.714V8H8v12.714z" fill={color in colors ? colors[color] : colors.gray} />
      <rect x="10" y="11" width="2" height="9" rx="1" fill="#fff" />
      <rect x="14" y="11" width="2" height="9" rx="1" fill="#fff" />
      <rect x="18" y="11" width="2" height="9" rx="1" fill="#fff" />
    </svg>
  );

  return (
    <StyledIcon component={DeleteOutlinedSVG} onClick={onClick} />
  );
};

DeleteOutlined.propTypes = {
  color: PropTypes.string,
  onClick: PropTypes.func,
};

DeleteOutlined.defaultProps = {
  color: colors.white,
  onClick: null,
};

export default DeleteOutlined;
