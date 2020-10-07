import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';
import colors from 'styles/colors';

const DeleteOutlined = ({ color, onClick }) => {
  const DeleteOutlinedSVG = () => (
    <svg width="16" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M11.813 1.125L10.687 0H5.064L3.938 1.125H0v2.25h15.75v-2.25h-3.938zM1 17.714C1 18.971 2.05 20 3.333 20h9.334C13.95 20 15 18.971 15 17.714V5H1v12.714z" fill="#AAA" />
      <rect x="3" y="8" width="2" height="9" rx="1" fill={color in colors ? colors[color] : colors.lightGray} />
      <rect x="7" y="8" width="2" height="9" rx="1" fill={color in colors ? colors[color] : colors.lightGray} />
      <rect x="11" y="8" width="2" height="9" rx="1" fill={color in colors ? colors[color] : colors.lightGray} />
    </svg>
  );

  return (
    <StyledIcon component={DeleteOutlinedSVG} onClick={onClick} className="anticon-delete-outlined" />
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
