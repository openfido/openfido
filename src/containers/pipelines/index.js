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

  const pipelineItemInEdit = pipelines && pipelines.find((pipelineItem) => pipelineItem.uuid === pipelineInEdit);

  useEffect(() => {
    dispatch(getPipelines(currentOrg));
    setShowGetStartedPopup(false);
  }, [currentOrg, dispatch]);

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
    dispatch(getPipelines(currentOrg))
      .then(() => setShowAddPipelines(false))
  };

  const handleAddPipelineCancel = () => {
    setShowAddPipelines(false);

    if (pipelines && !pipelines.length) {
      setShowGetStartedPopup(true);
    }
  };

  const openPipelineEdit = (pipeline_uuid) => {
    setPipelineInEdit(pipeline_uuid);
  };

  const handleEditPipelineSuccess = () => {
    dispatch(getPipelines(currentOrg))
      .then(() => setPipelineInEdit(null));
  };

  const handleEditPipelineCancel = () => {
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
        <EditPipeline
          handleSuccess={handleEditPipelineSuccess}
          handleCancel={handleEditPipelineCancel}
          pipelineItem={pipelineItemInEdit}
        />
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
              openPipelineEdit={openPipelineEdit}
            />
          ))}
        </PipelineItems>
      )}
      {showAddPipelines && (
        <AddPipeline
          handleSuccess={handleAddPipelineSuccess}
          handleCancel={handleAddPipelineCancel}
        />
      )}
    </>
  );
};

export default Pipelines;
