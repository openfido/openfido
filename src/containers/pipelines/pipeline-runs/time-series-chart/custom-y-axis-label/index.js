import React from 'react';
import PropTypes from 'prop-types';

import { Label } from 'recharts';

const CustomYAxisLabel = (props) => {
  const {
    viewBox,
  } = props;

  const {
    height, width, x,
  } = viewBox;

  return (
    <Label transform="rotate(-90)" y={50} x={x} height={height} width={width}>
      Energy Used (kWH)
    </Label>
  );
};

CustomYAxisLabel.propTypes = {
  viewBox: PropTypes.shape({
    height: PropTypes.number.isRequired,
    width: PropTypes.number.isRequired,
    x: PropTypes.number.isRequired,
    y: PropTypes.number.isRequired,
  }).isRequired,
};

export default CustomYAxisLabel;
