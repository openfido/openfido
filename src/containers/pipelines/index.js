import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import styled from 'styled-components';
import { Space } from 'antd';

import { getPipelines } from 'actions/pipelines';
import { StyledTitle, StyledButton } from 'styles/app';
import PipelineItem from './pipeline-item';
import CreatePipelinePopup from './get-started-popup';

const PipelineItems = styled(Space)`
  padding: 28px 20px 28px 16px;
  padding: 1.75rem 1.25rem 1.75rem 1rem;
`;

const Pipelines = () => {
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const pipelines = useSelector((state) => state.pipelines.pipelines);
  const dispatch = useDispatch();

  const [showGetStartedPopup, setShowGetStartedPopup] = useState(false);

  useEffect(() => {
    if (!pipelines) {
      dispatch(getPipelines(currentOrg));
    }
  }, [currentOrg, pipelines]);

  useEffect(() => {
    if (pipelines && !pipelines.length) {
      setShowGetStartedPopup(true);
    }
  }, [pipelines]);

  const closeGetStartedPopup = () => setShowGetStartedPopup(false);

  return (
    <>
      <StyledTitle>
        <div>
          <h1>Pipelines</h1>
          <StyledButton size="small">
            + Add Pipeline
          </StyledButton>
        </div>
      </StyledTitle>
      <Space direction="vertical" size={16}>
        {showGetStartedPopup && (
          <CreatePipelinePopup handleOk={closeGetStartedPopup} />
        )}
      </Space>
      <PipelineItems direction="vertical" size={26}>
        {pipelines && pipelines.map(({
          uuid, name, status, updated_at,
        }) => (
          <PipelineItem
            key={uuid}
            uuid={uuid}
            name={name}
            status={status}
            updated_at={updated_at}
          />
        ))}
      </PipelineItems>
    </>
  );
};

export default Pipelines;
