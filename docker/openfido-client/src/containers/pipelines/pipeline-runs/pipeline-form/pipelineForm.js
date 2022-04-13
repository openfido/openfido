import React, {
  useState, useEffect, useReducer,
} from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import {
  StyledButton,
} from 'styles/app';

import formReducer from 'reducers/configform';
import FormBuilder from './form-builder';

const PipelineFormStyled = styled.form`
  width: 70%;
  display: flex;
  flex-direction: column;
  align-items: left;
  padding-bottom: 10px;
`;

const DEFAULT_STATE = {};

const PipelineForm = ({
  config, formType, onInputFormSubmit, handleFormFieldUpload, uploadedCsv, onInputsChangedOrDropped,
}) => {
  const [fType, setFormType] = useState(undefined);
  const [fName, setFormName] = useState(undefined);

  // used to prepare the form for conversion
  const [formBuilder, setFormBuilder] = useState([]);
  const [isHidden, setIsHidden] = useState(false);
  const [toFile, dispatch] = useReducer(formReducer, DEFAULT_STATE);

  useEffect(() => {
    const [fname, type] = formType;
    setFormName(fname);
    setFormType(type);
  }, [formType]);

  // generates the provided fieldnames into an array
  // prepares form for file conversion and creates trackable state
  // if an item is provided with no details, generates generic field
  useEffect(() => {
    if (config === undefined) {
      setFormBuilder([]);
    } else {
      const configMapable = Object.keys(config);
      const cleanConfig = config;
      configMapable.map((item) => {
        if (cleanConfig[item].default === undefined) {
          cleanConfig[item].default = '';
        }
        if (cleanConfig[item].description === undefined) {
          cleanConfig[item].description = '';
        }
        if (cleanConfig[item].input_type === undefined) {
          cleanConfig[item].input_type = 'str';
        }
        if (cleanConfig[item].choices === undefined) {
          cleanConfig[item].choices = '';
        }
        if (cleanConfig[item].space_delimited !== true) {
          cleanConfig[item].space_delimited = false;
        }
        if (cleanConfig[item].upload_max === undefined) {
          cleanConfig[item].upload_max = 0;
        }
        if (cleanConfig[item].input_type.includes('required')) {
          cleanConfig[item].required = true;
          cleanConfig[item].isValidated = true;
        } else {
          cleanConfig[item].required = false;
          cleanConfig[item].isValidated = true;
        }
        cleanConfig[item].value = cleanConfig[item].default;
        cleanConfig[item].isOverMax = false;
        return item;
      });
      dispatch({
        type: 'HANDLE INITIAL UPDATE',
        payload: cleanConfig,
      });
      setFormBuilder(configMapable);
    }
  }, [config]);

  useEffect(() => {
    const csvData = uploadedCsv;
    csvData.map((item) => {
      if ((item.length > 0) && (config[item[0]] !== undefined)) {
        dispatch({
          type: 'HANDLE INPUT TEXT',
          field: item[0],
          payload: item[1],
        });
      }
      return item;
    });
  }, [uploadedCsv, config]);

  const clickHide = () => {
    // magic button to hide/unhide form
    setIsHidden(!isHidden);
  };

  // handy state update for majority of form needs
  const handleChange = (e) => {
    let update = e.target.value;
    if (config[e.target.id].input_type === 'boolean') {
      update = `${e.target.checked}`;
    }
    dispatch({
      type: 'HANDLE INPUT TEXT',
      field: e.target.id,
      payload: update,
    });
  };

  // converts the data selected into a proper csv-string before updating state
  // can be modified to make arrays for json version
  const handleChangeSelect = (data, id) => {
    let input = '';
    for (let i = 0; i < data.length; i += 1) {
      if (i === 0) {
        input = data[i].value;
      } else {
        input += `, ${data[i].value}`;
      }
    }
    dispatch({
      type: 'HANDLE INPUT TEXT',
      field: id,
      payload: input,
    });
  };

  const handleDrop = (e, id, space, max) => {
    let update = '';
    const files = Array.from(e.target.files || e.dataTransfer.files);
    if (max) {
      if (files.length > max) {
        dispatch({
          type: 'DROPPED OVER MAXIMUM ALLOWED',
          field: id,
          payload: true,
        });
      } else {
        dispatch({
          type: 'DROPPED OVER MAXIMUM ALLOWED',
          field: id,
          payload: false,
        });
      }
      if (max === 1) {
        update = files[0].name;
      } else {
        for (let i = 0; i < max; i += 1) {
          if (i === (max - 1)) {
            update += files[i].name;
          } else if (space) {
            update += `${files[i].name} `;
          } else {
            update += `${files[i].name}, `;
          }
        }
      }
      handleFormFieldUpload(e, max);
    } else {
      onInputsChangedOrDropped(e);
      for (let i = 0; i < files.length; i += 1) {
        if (space) {
          update += `${files[i].name} `;
        } else {
          update += `${files[i].name}, `;
        }
      }
    }
    dispatch({
      type: 'HANDLE INPUT TEXT',
      field: id,
      payload: update,
    });
  };

  const formValidator = (configMapable) => {
    // do magic;
    let passing = true;
    for (let i = 0; i < configMapable.length; i += 1) {
      if (toFile[configMapable[i]].required) {
        if (toFile[configMapable[i]].value.length === 0) {
          dispatch({
            type: 'HANDLE VALIDATION',
            field: configMapable[i],
            payload: false,
          });
          passing = false;
        } else if (toFile[configMapable[i]].isValidated === false) {
          dispatch({
            type: 'HANDLE VALIDATION',
            field: configMapable[i],
            payload: true,
          });
          passing = true;
        }
      }
    }
    return passing;
  };

  // combined csv and rc generation due to similarities and for easier/cleaner maintenance
  const handleUpload = (configMapable, datatype) => {
    const temp = [];
    configMapable.map((item) => {
      if (toFile[item].input_type === 'title') {
        return item;
      }
      if (fType === 'rc') {
        temp.push([
          toFile[item].value,
        ]);
      }
      if (fType === 'csv') {
        temp.push([
          item, toFile[item].value,
        ]);
      }
      return item;
    });
    const fileContent = temp.map((e) => e.join(',')).join('\n');
    const file = new Blob([fileContent], { // eslint-disable-line
      type: datatype,
    });
    onInputFormSubmit(file, `${fName}.${fType}`);
  };

  // Json has unique complications, therefore gets its own handler.
  const convertToJson = (configMapable) => {
    const temp = {};
    configMapable.map((item) => {
      if (toFile[item].input_type === 'title') {
        return item;
      }
      if (toFile[item].input_type === 'arr') {
        temp[item] = toFile[item].value.split(',');
        return item;
      }
      if (toFile[item].input_type === 'boolean') {
        if (toFile[item].value === 'true') {
          temp[item] = true;
          return item;
        }
        temp[item] = false;
        return item;
      }
      temp[item] = toFile[item].value;
      return item;
    });
    const fileContent = JSON.stringify(temp);
    const file = new Blob([fileContent], { // eslint-disable-line
      type: 'application/json',
    });
    onInputFormSubmit(file, `${fName}.${fType}`);
  };

  // adjusts applicable parameters based on the received form
  const handleSubmit = async () => {
    const configMapable = Object.keys(config);
    if (formValidator(configMapable)) {
      if (configMapable === undefined) {
      alert('There was an error with the configuration file'); // eslint-disable-line
      } else if (fType === 'csv') {
        handleUpload(configMapable, 'text/csv');
      } else if (fType === 'rc') {
        handleUpload(configMapable, 'text/plain');
      } else if (fType === 'json') {
        convertToJson(configMapable);
      }
      clickHide();
    }
  };

  // generates a form based on the length of the config file
  if (formBuilder.length > 0 && (typeof (fType) === 'string')) {
    return (
      <PipelineFormStyled>
        <StyledButton
          type="text"
          size="middle"
          textcolor="lightBlue"
          onClick={(e) => clickHide(e)}
        >
          <div>
            <strong>
              Manually fill the
              {' "'}
              {fName}
              {'" '}
              form
            </strong>
          </div>
        </StyledButton>
        <div style={isHidden ? {} : { display: 'none' }}>
          {formBuilder.map((item) => {
            const field = toFile[item];
            let fieldName;
            let fieldId = '';
            if (toFile[item].prompt === undefined) {
              fieldName = item;
            } else {
              fieldName = toFile[item].prompt;
            }
            if (typeof (item) === 'string') {
              fieldId = item;
            }
            return (
              <FormBuilder
                key={item}
                type={fType}
                field={field}
                fieldId={fieldId}
                fieldName={fieldName}
                value={toFile[item]}
                handleChange={handleChange}
                handleChangeSelect={handleChangeSelect}
                handleFormFieldUpload={handleFormFieldUpload}
                handleDrop={handleDrop}
              />
            );
          })}
          <StyledButton type="submit" onClick={() => handleSubmit()}>Submit form</StyledButton>
        </div>
      </PipelineFormStyled>
    );
  }
  return (
    <div />
  );
};

PipelineForm.propTypes = {
  config: PropTypes.shape({
    root: PropTypes.string,
  }).isRequired,
  onInputFormSubmit: PropTypes.func.isRequired,
  handleFormFieldUpload: PropTypes.func.isRequired,
  onInputsChangedOrDropped: PropTypes.func.isRequired,
  formType: PropTypes.arrayOf(PropTypes.string).isRequired,
  uploadedCsv: PropTypes.arrayOf(PropTypes.array).isRequired,
};

export default PipelineForm;
