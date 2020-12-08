import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';
import colors from 'styles/colors';

const UserFilled = ({ color, onClick }) => {
  const UserFilledSVG = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill={color in colors ? colors[color] : colors.lightGray}>
      <path d="M27 24.237V27a1 1 0 01-1 1H5a1 1 0 01-1-1v-2.763a1.578 1.578 0 01.931-1.365l5.136-2.705A5.024 5.024 0 0014.553 23h1.894a5.023 5.023 0 004.486-2.833l5.136 2.705A1.578 1.578 0 0127 24.237zM9.645 14.126a2.991 2.991 0 001.31 1.462l.666 3.051A3 3 0 0014.552 21h1.896a3 3 0 002.93-2.36l.666-3.052a2.991 2.991 0 001.311-1.462l.28-.752A1.275 1.275 0 0021 11.63V9c0-3-2-5-5.5-5S10 6 10 9v2.63a1.275 1.275 0 00-.635 1.744z" />
    </svg>
  );

  return (
    <StyledIcon component={UserFilledSVG} onClick={onClick} className="anticon-user" />
  );
};

UserFilled.propTypes = {
  color: PropTypes.string,
  onClick: PropTypes.func,
};

UserFilled.defaultProps = {
  color: colors.white,
  onClick: null,
};

export default UserFilled;
