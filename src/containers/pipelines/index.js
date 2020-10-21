import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import styled from 'styled-components';
import { Space } from 'antd';

import { getPipelines } from 'actions/pipelines';
import { StyledTitle, StyledButton } from 'styles/app';
import PipelineItem from './pipeline-item';
import CreatePipelinePopup from './get-started-popup';
import AddPipeline from './add-pipeline';
import EditPipeline from './edit-pipeline';

const PipelineItems = styled(Space)`
  padding: 28px 20px 28px 16px;
  padding: 1.75rem 1.25rem 1.75rem 1rem;
`;

const Pipelines = () => {
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const pipelines = useSelector((state) => state.pipelines.pipelines);
  const dispatch = useDispatch();

  const [showGetStartedPopup, setShowGetStartedPopup] = useState(false);
  const [showAddPipelines, setShowAddPipelines] = useState(false);
  const [pipelineInEdit, setPipelineInEdit] = useState(null);

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

  const openAddPipelines = () => {
    setShowGetStartedPopup(false);
    setShowAddPipelines(true);
  };

  const handleAddPipelineSuccess = () => {
    setShowAddPipelines(false);
    dispatch(getPipelines(currentOrg));
  };

  const handlePipelineEdit = (pipeline_uuid) => {
    setPipelineInEdit(pipeline_uuid);
  };

  const handleEditPipelineSuccess = () => {
    setPipelineInEdit(null);
  };

  return (
    <>
      <StyledTitle>
        <div>
          <h1>Pipelines</h1>
          <StyledButton size="small" onClick={openAddPipelines}>
            + Add Pipeline
          </StyledButton>
        </div>
      </StyledTitle>
      <Space direction="vertical" size={16}>
        {showGetStartedPopup && (
          <CreatePipelinePopup handleOk={openAddPipelines} />
        )}
      </Space>
      {!showAddPipelines && pipelineInEdit && (
        <EditPipeline handleSuccess={handleEditPipelineSuccess} pipelineItem={pipelineInEdit} />
      )}
      {!showAddPipelines && !pipelineInEdit && (
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
              handlePipelineEdit={handlePipelineEdit}
            />
          ))}
        </PipelineItems>
      )}
      {showAddPipelines && (
        <AddPipeline handleSuccess={handleAddPipelineSuccess} />
      )}
    </>
  );
};

export default Pipelines;
