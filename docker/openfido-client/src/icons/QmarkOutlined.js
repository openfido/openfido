import React from 'react';
import PropTypes from 'prop-types';

import { StyledQmark } from 'styles/app';

const QmarkOutlined = ({ onClick }) => {
  const QuestionOutlinedSVG = () => (
    <svg width="24px" height="24px" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" clipRule="evenodd" d="M1.917 11.5c0-5.29 4.293-9.583 9.583-9.583s9.584 4.293 9.584 9.583-4.294 9.583-9.584 9.583S1.917 16.79 1.917 11.5zm7.667 2.08l6.315-6.316 1.351 1.361-7.666 7.667-3.834-3.834 1.352-1.351 2.482 2.473z" fill="#F27F58" />
      <g data-name="Layer 2">
        <g data-name="menu-arrow-circle">
          <rect width="24" height="24" transform="rotate(180 12 12)" opacity="0" />
          <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 16a1 1 0 1 1 1-1 1 1 0 0 1-1 1zm1-5.16V14a1 1 0 0 1-2 0v-2a1 1 0 0 1 1-1 1.5 1.5 0 1 0-1.5-1.5 1 1 0 0 1-2 0 3.5 3.5 0 1 1 4.5 3.34z" />
        </g>
      </g>
    </svg>
  );

  return (
    <StyledQmark component={QuestionOutlinedSVG} onClick={onClick} />
  );
};

QmarkOutlined.propTypes = {
  onClick: PropTypes.func,
};

QmarkOutlined.defaultProps = {
  onClick: null,
};

export default QmarkOutlined;
