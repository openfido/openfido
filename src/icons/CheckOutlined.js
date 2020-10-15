import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';
import colors from 'styles/colors';

const CheckOutlined = ({ color, onClick }) => {
  const CheckOutlinedSVG = () => (
    <svg width="23" height="23" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path fillRule="evenodd" clipRule="evenodd" d="M11.5 1.917c-5.29 0-9.584 4.293-9.584 9.583s4.294 9.583 9.584 9.583 9.583-4.293 9.583-9.583S16.79 1.917 11.5 1.917zm0 17.25c-4.226 0-7.667-3.44-7.667-7.667 0-4.226 3.44-7.667 7.667-7.667 4.226 0 7.666 3.44 7.666 7.667 0 4.226-3.44 7.667-7.666 7.667zm-1.917-5.588L15.9 7.264l1.35 1.361-7.666 7.667-3.833-3.834L7.1 11.107l2.482 2.473z" fill="#000" fillOpacity=".54" />
    </svg>
  );

  return (
    <StyledIcon component={CheckOutlinedSVG} onClick={onClick} />
  );
};

CheckOutlined.propTypes = {
  color: PropTypes.string,
  onClick: PropTypes.func,
};

CheckOutlined.defaultProps = {
  color: colors.white,
  onClick: null,
};

export default CheckOutlined;
