import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';
import colors from 'styles/colors';

const CloudOutlined = ({ color, onClick }) => {
  const CloudOutlinedSVG = () => (
    <svg width="95" height="95" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" clipRule="evenodd" d="M76.594 39.742C73.902 26.085 61.908 15.833 47.5 15.833c-11.44 0-21.375 6.492-26.323 15.992C9.262 33.092 0 43.185 0 55.417c0 13.102 10.648 23.75 23.75 23.75h51.458C86.133 79.167 95 70.3 95 59.375c0-10.45-8.115-18.92-18.406-19.633zM75.208 71.25H23.75c-8.748 0-15.833-7.085-15.833-15.833 0-8.115 6.056-14.884 14.091-15.715l4.236-.435 1.979-3.76C31.983 28.261 39.346 23.75 47.5 23.75c10.37 0 19.317 7.362 21.335 17.535l1.188 5.938 6.056.435c6.175.396 11.004 5.581 11.004 11.717 0 6.531-5.343 11.875-11.875 11.875zM41.76 51.458H31.667L47.5 35.625l15.833 15.833H53.24v11.875H41.76V51.458z" fill={color in colors ? colors[color] : colors.gray} />
    </svg>
  );

  return (
    <StyledIcon component={CloudOutlinedSVG} onClick={onClick} className="anticon-close-outlined" />
  );
};

CloudOutlined.propTypes = {
  color: PropTypes.string,
  onClick: PropTypes.func,
};

CloudOutlined.defaultProps = {
  color: colors.white,
  onClick: null,
};

export default CloudOutlined;
