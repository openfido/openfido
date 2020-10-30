import React from 'react';
import { Spin } from 'antd';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import { pipelineStates, statusLongNameLegend } from 'config/pipeline-status';
import LoadingFilled from 'icons/LoadingFilled';
import DownloadFilled from 'icons/DownloadFilled';
import { StyledH3, StyledText } from 'styles/app';
import colors from 'styles/colors';

const StyledFilesList = styled.div`
  .anticon.anticon-download {
    margin-right: 4px;
    margin-right: 0.25rem;
    margin-left: -4px;
    margin-left: -0.25rem;
  }
  h3 {
    margin-left: 0.25rem;
    margin-top: 1rem;
    display: flex;
    justify-content: space-between;
  }
  ul {
    list-style-type: none;
    padding: 0;
    margin: 16px 0;
    margin: 1rem 0;
    li {
      display: flex;
      justify-content: space-between;
      font-size: 16px;
      font-size: 1rem;
      line-height: 19px;
      line-height: 1.195rem;
      padding: 12px 0 12px 4px;
      padding: 0.75rem 0 0.75rem 0.25rem;
      color: ${colors.gray};
      white-space: nowrap;
      a {
        overflow: hidden;
        text-overflow: ellipsis;
        margin-right: 8px;
        margin-right: 0.5rem;
        color: ${colors.mediumBlue};
        font-weight: 500;
        &:hover {
          color: ${colors.lightBlue};
          .anticon.anticon-download svg path {
            fill: ${colors.lightBlue};
            fill-opacity: 1.0;
          }
        }
      }
      > span {
        min-width: 56px;
        max-width: 56px;
      }
      > div {
        display: block;
        .anticon {
          right: -25px;
        }
      }
    }
  }
`;

const OverviewMeta = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  position: relative;
`;

const FilesList = ({ title, files, pipelineRunSelected: run }) => {
  const runStatus = run && run.states && run.states.length && run.states[0].state;

  return (
    <StyledFilesList>
      <StyledH3 color="black">
        <span>{title}</span>
        <span>Size</span>
      </StyledH3>
      {files && files.length ? (
        <ul>
          {files && files.map(({
            uuid, name: file_name, url, size,
          }) => (
            <li key={uuid}>
              <a href={url} rel="noreferrer" target="_blank" title={file_name}>
                <DownloadFilled />
                {file_name}
              </a>
              <span>{size}</span>
            </li>
          ))}
        </ul>
      ) : (
        <ul>
          <li>
            <OverviewMeta>
              <StyledText size="large" color="black" fontweight={500}>
                {statusLongNameLegend[runStatus]}
              </StyledText>
              {runStatus === pipelineStates.RUNNING && (
                <Spin indicator={<LoadingFilled spin />} />
              )}
            </OverviewMeta>
          </li>
        </ul>
      )}
    </StyledFilesList>
  );
};

FilesList.propTypes = {
  title: PropTypes.string.isRequired,
  files: PropTypes.arrayOf(PropTypes.shape({
    uuid: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
  })).isRequired,
  pipelineRunSelected: PropTypes.shape({
    sequence: PropTypes.number.isRequired,
    updated_at: PropTypes.string.isRequired,
    started_at: PropTypes.string.isRequired,
    created_at: PropTypes.string.isRequired,
    states: PropTypes.arrayOf(PropTypes.shape({
      state: PropTypes.string.isRequired,
    })),
  }).isRequired,
};

export default FilesList;
