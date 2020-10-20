import React from 'react';
import PropTypes from 'prop-types';

import { StyledIcon } from 'styles/app';

const CheckFilled = ({ onClick }) => {
  const CheckFilledSVG = () => (
    <svg width="23" height="23" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" clipRule="evenodd" d="M1.917 11.5c0-5.29 4.293-9.583 9.583-9.583s9.584 4.293 9.584 9.583-4.294 9.583-9.584 9.583S1.917 16.79 1.917 11.5zm7.667 2.08l6.315-6.316 1.351 1.361-7.666 7.667-3.834-3.834 1.352-1.351 2.482 2.473z" fill="#F27F58" />
    </svg>
  );

  return (
    <StyledIcon component={CheckFilledSVG} onClick={onClick} />
  );
};

CheckFilled.propTypes = {
  onClick: PropTypes.func,
};

CheckFilled.defaultProps = {
  onClick: null,
};

export default CheckFilled;
