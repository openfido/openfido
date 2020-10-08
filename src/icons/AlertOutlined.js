import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';
import colors from 'styles/colors';

const AlertOutlined = ({ color, onClick }) => {
  const AlertOutlinedSVG = () => (
    <svg width="18" height="16" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" clipRule="evenodd" d="M.75 15.125L9 .875l8.25 14.25H.75zm13.897-1.5L9 3.867l-5.648 9.758h11.295zm-6.397-2.25v1.5h1.5v-1.5h-1.5zm0-4.5h1.5v3h-1.5v-3z" fill="#E96D47" />
    </svg>
  );

  return (
    <StyledIcon component={AlertOutlinedSVG} onClick={onClick} className="anticon-delete-outlined" />
  );
};

AlertOutlined.propTypes = {
  color: PropTypes.string,
  onClick: PropTypes.func,
};

AlertOutlined.defaultProps = {
  color: colors.white,
  onClick: null,
};

export default AlertOutlined;
