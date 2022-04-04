import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';

import { requestStartPipelineRun } from 'services';
import {
  uploadInputFile,
  removeInputFile,
  clearInputFiles,
} from 'actions/pipelines';
import CloseOutlined from 'icons/CloseOutlined';
import CloudOutlined from 'icons/CloudOutlined';
import {
  StyledModal,
  StyledButton,
  StyledText,
} from 'styles/app';
import colors from 'styles/colors';
import gitApi from 'util/api-github';
import PipelineForm from '../pipeline-form/pipelineForm';

const Modal = styled(StyledModal)`
  h2 {
    text-transform: uppercase;
    color: ${colors.black};
    text-align: center;
    line-height: 32px;
    line-height: 2rem;
    margin-bottom: 32px;
  }
  .anticon-close-outlined {
    top: 8px;
    right: 12px;
  }
  .ant-modal-body {
    padding: 24px 0;
    border-radius: 6px;
    background-color: ${colors.lightBg};
  }
`;

const StyledForm = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  input[type="file"] {
    display: none;
  }
`;

const UploadBox = styled.div`
  border: 2px dashed ${colors.gray};
  border-radius: 3px;
  position: relative;
  margin-left: 1px;
  &:after {
    content: '';
    position: absolute;
    left: -1px;
    top: -1px;
    right: -1px;
    bottom: -1px;
    border: 1px solid ${colors.lightBg};
    pointer-events: none;
  }
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  height: 169px;
  padding: 8px 20px 20px 20px;
  .anticon {
    position: static;
  }
  .ant-btn label {
    padding: 0;
  }
  &.dragged {
    border-color: ${colors.lightBlue};
    svg path {
      fill: ${colors.lightBlue};
    }
  }
`;

export const UploadSection = styled.div`
  width: 100%;
  padding: 0 42px 16px 36px;
  padding: 0 2.625rem 1.75rem 2.25rem;
  border-bottom: 1px solid ${colors.grey};
`;

const ArtifactsSection = styled.div`
  > div {
    margin: 24px 36px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 48px;
    grid-row-gap: 24px;
    grid-row-gap: 1.5rem;
    grid-column-gap: 88px;
    grid-column-gap: 5.5rem;
  }
  margin-bottom: 24px;
  margin-bottom: 1.5rem;
  max-height: 33vh;
  overflow: overlay;
`;

export const Artifact = styled.div`
  background-color ${colors.white};
  color: ${colors.black};
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 16px 4px 24px;
  padding: 0.25rem 1rem 0.25rem 1.5rem;
  font-size: 16px;
  line-height: 19px;
  width: 261px;
  height: 48px;
  max-height: 48px;
  cursor: pointer;
  position: relative;
  span:first-child {
    margin-right: 8px;
    margin-right: 0.5rem;
    white-space: pre;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .anticon {
    position: static;
    float: right;
    svg {
      width: 18px;
      width: 1.125rem;
      height: 18px;
      height: 1.125rem;
    }
  }
  &:hover {
    .anticon svg line {
      stroke: ${colors.gray20};
    }
  }
`;

const StartRunPopup = ({
  handleOk, handleCancel, pipeline_uuid, configUrl, piplineUrl, pipelineBranch,
}) => {
  const currentOrg = useSelector((state) => state.user.currentOrg);
  const dispatch = useDispatch();

  const inputFiles = useSelector((state) => state.pipelines.inputFiles);
  const [uploadBoxDragged, setUploadBoxDragged] = useState(false);

  const [manifest, setManifest] = useState(null);
  const [manual, setManual] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedCsv, setUploadedCsv] = useState([]);

  useEffect(() => {
    // uses the passed-in URL to grab the manifest
    // Object.keys(response.manual) to determine which forms to build
    gitApi.getManifest(configUrl, pipelineBranch)
      .then((response) => {
        if (response.manual === undefined) {
          console.log('Missing manual property from the manifest');
        } else {
          setManifest(response);
          setManual(Object.keys(response.manual));
        }
      }, (error) => {
        console.log(error);
      });
  }, [configUrl, pipelineBranch]);

  // When file(s) selected from browse, or dropped on the box, disable start run until
  // files are done uploading to the pipeline
  const onInputsChangedOrDropped = (e) => {
    e.preventDefault();
    let uploadCounter = 0;

    Array.from(e.target.files || e.dataTransfer.files).forEach((file, index, array) => {
      const fileReader = new window.FileReader();
      // added loadend event to enable autofill matching form fields with uploaded config
      fileReader.addEventListener('loadend', (event) => {
        if (file.name === 'config.csv') {
          const buf = event.target.result;
          let view = String.fromCharCode.apply(null, new Int8Array(buf)).split('\n');
          view = view.map((item) => {
            const temp = [];
            const splitter = item.split(',');
            temp.push(splitter.shift());
            temp.push(splitter.join(',').replace('\r', ''));
            return temp;
          });
          setUploadedCsv(view);
        }
      });
      fileReader.addEventListener('loadstart', () => {
        setIsLoading(true);
      });
      fileReader.onload = () => {
        dispatch(uploadInputFile(currentOrg, pipeline_uuid, file.name, fileReader.result))
          .then(() => {
            uploadCounter += 1;
            if (uploadCounter === array.length) {
              setIsLoading(false);
            }
          });
      };

      fileReader.readAsArrayBuffer(file);
    });

    if (uploadBoxDragged) setUploadBoxDragged(false);
  };

  const onUploadBoxDragOverOrEnter = (e) => {
    e.preventDefault();

    if (!uploadBoxDragged) setUploadBoxDragged(true);
  };

  const onUploadBoxDragLeave = () => {
    if (uploadBoxDragged) setUploadBoxDragged(false);
  };

  const onStartRunClicked = () => {
    const inputUuids = [];

    if (inputFiles) {
      inputFiles.forEach(({ uuid: input_uuid }) => {
        inputUuids.push(input_uuid);
      });
    }
    requestStartPipelineRun(currentOrg, pipeline_uuid, inputUuids)
      .then(() => {
        handleOk(true);
        dispatch(clearInputFiles());
      });
  };

  const onRemoveInputFileClicked = (index) => {
    dispatch(removeInputFile(index));
  };

  // clears input files on closing the modal to prevent cross contamination
  const onCloseStartRunPopup = () => {
    handleCancel();
    dispatch(clearInputFiles());
  };

  // passed into the form generators to upload the processed form data into the pipeline
  const handleInputFormSubmit = async (data, fileName) => {
    const fileReader = new window.FileReader();
    fileReader.addEventListener('loadstart', () => {
      setIsLoading(true);
    });
    fileReader.addEventListener('loadend', () => {
      setIsLoading(false);
    });
    fileReader.onload = () => {
      dispatch(uploadInputFile(currentOrg, pipeline_uuid, fileName, fileReader.result));
    };

    fileReader.readAsArrayBuffer(data);
  };

  const handleFormFieldUpload = (e) => {
    e.preventDefault();
    let file;

    if (e.target.files) {
      [file] = e.target.files;
    } else if (e.dataTransfer.files) {
      [file] = e.dataTransfer.files;
    }

    const fileReader = new window.FileReader();
    fileReader.addEventListener('loadstart', () => {
      setIsLoading(true);
    });
    fileReader.onload = () => {
      dispatch(uploadInputFile(currentOrg, pipeline_uuid, file.name, fileReader.result))
        .then(() => setIsLoading(false));
    };

    fileReader.readAsArrayBuffer(file);
  };

  const handleOpenPiplineClick = () => {
    window.open(piplineUrl);
  };

  return (
    <Modal
      visible
      footer={[
        <StyledButton
          type="text"
          size="middle"
          textcolor="lightBlue"
          onClick={handleOpenPiplineClick}
        >
          Help
        </StyledButton>,
      ]}
      onOk={handleOk}
      onCancel={onCloseStartRunPopup}
      closeIcon={<CloseOutlined color="darkText" />}
      width={690}
      maskStyle={{ top: '82px', left: '250px' }}
      style={{ position: 'absolute', top: '179px', left: 'calc(((100vw - 690px + 250px) / 2))' }}
      title="Start a run"
    >
      <StyledForm onSubmit={onStartRunClicked}>
        {
          manual.map((item) => {
            // Don't attempt a render if there is nothing to render yet
            if (manual.length === 0) {
              return <div />;
            }
            return (
              <PipelineForm
                config={manifest[item]}
                key={item}
                formType={[item, manifest.manual[item]]}
                onInputFormSubmit={(arrayBuffer, fileName) => handleInputFormSubmit(arrayBuffer, fileName)}
                handleFormFieldUpload={handleFormFieldUpload}
                uploadedCsv={uploadedCsv}
              />
            );
          })
        }
        <UploadSection>
          <UploadBox
            onDragOver={onUploadBoxDragOverOrEnter}
            onDragEnter={onUploadBoxDragOverOrEnter}
            onDragLeave={onUploadBoxDragLeave}
            onDrop={onInputsChangedOrDropped}
            className={uploadBoxDragged ? 'dragged' : ''}
          >
            <CloudOutlined />
            <div>
              <StyledText size="large" color="darkText">
                Drag and drop your input file here, or
                {' '}
                <StyledButton
                  type="text"
                  size="middle"
                  textcolor="lightBlue"
                >
                  <label>
                    <input type="file" onChange={onInputsChangedOrDropped} multiple />
                    <strong>browse</strong>
                  </label>
                </StyledButton>
                .
              </StyledText>
            </div>
          </UploadBox>
        </UploadSection>
        <ArtifactsSection>
          <div>
            {inputFiles && inputFiles.map(({ name: input_name }, index) => (
              <Artifact key={`${input_name}${Math.random()}`} title={input_name}>
                <StyledText>{input_name}</StyledText>
                <CloseOutlined color="lightGray" onClick={() => onRemoveInputFileClicked(index)} />
              </Artifact>
            ))}
          </div>
        </ArtifactsSection>
        <StyledButton
          disabled={isLoading}
          aria-label="Start Run button"
          size="middle"
          color="blue"
          width={108}
          onClick={onStartRunClicked}
        >
          Start Run
        </StyledButton>
      </StyledForm>
    </Modal>
  );
};

StartRunPopup.propTypes = {
  handleOk: PropTypes.func.isRequired,
  handleCancel: PropTypes.func.isRequired,
  pipeline_uuid: PropTypes.string.isRequired,
  pipelineBranch: PropTypes.string.isRequired,
  piplineUrl: PropTypes.string.isRequired,
  configUrl: PropTypes.string.isRequired,
};

export default StartRunPopup;
