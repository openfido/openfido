import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';
import colors from 'styles/colors';

const MailOutlined = ({ color, onClick }) => {
  const MailOutlinedSVG = () => (
    <svg width="39" height="31" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" clipRule="evenodd" d="M38.5 4.05A3.861 3.861 0 0034.65.2H3.85A3.861 3.861 0 000 4.05v23.1A3.861 3.861 0 003.85 31h30.8a3.861 3.861 0 003.85-3.85V4.05zm-3.85 0l-15.4 9.625L3.85 4.05h30.8zm-30.8 23.1h30.8V7.9l-15.4 9.625L3.85 7.9v19.25z" fill={color in colors ? colors[color] : colors.lightGray} />
    </svg>
  );

  return (
    <StyledIcon component={MailOutlinedSVG} onClick={onClick} className="anticon-mail" />
  );
};

MailOutlined.propTypes = {
  color: PropTypes.string,
  onClick: PropTypes.func,
};

MailOutlined.defaultProps = {
  color: colors.white,
  onClick: null,
};

export default MailOutlined;
