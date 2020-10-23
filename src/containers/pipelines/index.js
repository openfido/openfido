import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import styled from 'styled-components';
import { Space } from 'antd';

import { getPipelines } from 'actions/pipelines';
import { StyledTitle, StyledButton, StyledText } from 'styles/app';
import PipelineItem from './pipeline-item';
import CreatePipelinePopup from './get-started-popup';
import AddPipeline from './add-pipeline';
import EditPipeline from './edit-pipeline';
import PipelineRuns from './pipeline-runs';

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
  const [pipelineInView, setPipelineInView] = useState(null);

  const pipelineItemInEdit = pipelines && pipelines.find((pipelineItem) => pipelineItem.uuid === pipelineInEdit);
  const pipelineItemInView = pipelines && pipelines.find((pipelineItem) => pipelineItem.uuid === pipelineInView);

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
      .then(() => setShowAddPipelines(false));
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

  const viewPipelineRuns = (pipeline_uuid) => {
    setPipelineInView(pipeline_uuid);
  };

  return (
    <>
      <StyledTitle>
        <div>
          <h1>
            {pipelineInView && pipelineItemInView ? (
              <>
                Pipeline Runs:
                {' '}
                <StyledText color="blue">{pipelineItemInView.name}</StyledText>
              </>
            ) : (
              <>
                Pipelines
                <StyledButton size="small" onClick={openAddPipelines}>
                  + Add Pipeline
                </StyledButton>
              </>
            )}
          </h1>
        </div>
      </StyledTitle>
      <Space direction="vertical" size={16}>
        {showGetStartedPopup && (
          <CreatePipelinePopup handleOk={openAddPipelines} />
        )}
      </Space>
      {showAddPipelines && (
      <AddPipeline
        handleSuccess={handleAddPipelineSuccess}
        handleCancel={handleAddPipelineCancel}
      />
      )}
      {!showAddPipelines && pipelineInEdit && (
        <EditPipeline
          handleSuccess={handleEditPipelineSuccess}
          handleCancel={handleEditPipelineCancel}
          pipelineItem={pipelineItemInEdit}
        />
      )}
      {!showAddPipelines && !pipelineInView && !pipelineInEdit && (
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
              viewPipelineRuns={viewPipelineRuns}
            />
          ))}
        </PipelineItems>
      )}
      {!showAddPipelines && pipelineInView && (
        <PipelineRuns
          pipelineInView={pipelineInView}
        />
      )}
    </>
  );
};

export default Pipelines;
