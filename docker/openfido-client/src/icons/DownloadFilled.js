import React from 'react';
import PropTypes from 'prop-types';
import Icon from '@ant-design/icons';

const DownloadFilled = ({ onClick }) => {
  const DownloadFilledSVG = () => (
    <svg width="19" height="19" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fillRule="evenodd" clipRule="evenodd" d="M10.292 10.767h2.375L9.5 13.933l-3.167-3.166h2.375V2.85h1.584v7.917zm-7.125 6.016V15.2h12.666v1.583H3.167z" fill="#000" fillOpacity=".54" />
    </svg>
  );

  return (
    <Icon component={DownloadFilledSVG} onClick={onClick} className="anticon-download" />
  );
};

DownloadFilled.propTypes = {
  onClick: PropTypes.func,
};

DownloadFilled.defaultProps = {
  onClick: null,
};

export default DownloadFilled;
