import React from 'react';
import PropTypes from 'prop-types';
import Icon from '@ant-design/icons';

import colors from 'styles/colors';

const DownOutlined = (props) => {
  const { color } = props;

  const DownOutlinedSVG = () => (
    <svg width="11" height="7" viewBox="0 0 11 7" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M10.9241 1.81998L5.85239 6.85573C5.65847 7.04809 5.34521 7.04809 5.15129 6.85573L0.0745844 1.81998C-0.0248615 1.72133 -0.0248615 1.56843 0.0745844 1.46979L1.48174 0.0739827C1.58119 -0.0246609 1.73533 -0.0246609 1.83478 0.0739827L5.50433 3.71393L9.17388 0.0739827C9.27332 -0.0246609 9.42746 -0.0246609 9.52691 0.0739827L10.9341 1.46979C11.0236 1.56843 11.0236 1.72626 10.9241 1.81998Z" fill={color in colors ? colors[color] : colors.white} />
    </svg>
  );

  return (
    <Icon component={DownOutlinedSVG} />
  );
};

DownOutlined.propTypes = {
  color: PropTypes.string,
};

DownOutlined.defaultProps = {
  color: colors.white,
};

export default DownOutlined;
