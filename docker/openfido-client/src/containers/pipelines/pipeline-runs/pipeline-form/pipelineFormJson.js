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

const PipelineFormJson = ({ config, formType, onInputFormSubmit }) => {
  const [fType, setFormType] = useState(null);
  const [fName, setFormName] = useState(null);
  // used to prepare the form for conversion
  const [formBuilder, setFormBuilder] = useState([]);
  const [isHidden, setIsHidden] = useState(false);
  const [toJson, dispatch] = useReducer(formReducer, DEFAULT_STATE);

  useEffect(() => {
    const [fname, type] = formType;
    setFormName(fname);
    setFormType(type);
  }, [formType]);

  // generates the provided fieldnames into an array
  // prepares form for json conversion and creates trackable state
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
        if (cleanConfig[item].descrition === undefined) {
          cleanConfig[item].description = '';
        }
        cleanConfig[item].value = cleanConfig[item].default;
        return item;
      });
      dispatch({
        type: 'HANDLE INITIAL UPDATE',
        payload: cleanConfig,
      });
      setFormBuilder(configMapable);
    }
  }, [config]);

  const clickHide = () => {
    // magic button to hide/unhide form
    setIsHidden(!isHidden);
  };

  const handleChange = (e) => {
    dispatch({
      type: 'HANDLE INPUT TEXT',
      field: e.target.id,
      payload: e.target.value,
    });
  };

  // const formValidator = (configMapable) => {
  //   // do magic;
  //   let passing = true;
  //   for (let i = 0; i < configMapable.length; i += 1) {
  //     console.log(toJson[configMapable[i]]);
  //     if (toJson[configMapable[i]].input_type.contains('required')) {
  //       if (toJson[configMapable[i]].value.length === 0) {
  //         alert(`Please enter a value in the ${configMapable[i]} field`);
  //         passing = false;
  //         break;
  //       }
  //     }
  //   }
  //   return passing;
  // }; if (formValidator(configMapable))

  const convertToJson = (configMapable) => {
    const temp = {};
    configMapable.map((item) => {
      if (toJson[item].input_type === 'title') {
        return item;
      }
      if (toJson[item].input_type === 'arr') {
        temp[item] = toJson[item].value.split(',');
        return item;
      }
      if (toJson[item].input_type === 'boolean') {
        if (toJson[item].value === 'true') {
          temp[item] = true;
          return item;
        }
        temp[item] = false;
        return item;
      }
      temp[item] = toJson[item].value;
      return item;
    });
    const fileContent = `data:application/json;charset=utf-8,${JSON.stringify(temp)}`;
    const file = new Blob([fileContent], { // eslint-disable-line
      type: 'application/json',
    });
    onInputFormSubmit(file, `${fName}.${fType}`);
    const encodedUri = encodeURI(fileContent);
    const link = document.createElement('a'); // eslint-disable-line
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `${fName}.${fType}`);
    document.body.appendChild(link); // eslint-disable-line
    link.click(); // This will download the data file named "my_data.rc".
  };

  const handleSubmit = async () => {
    const configMapable = Object.keys(config);
    convertToJson(configMapable);
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
            const field = config[item];
            let fieldName;
            if (config[item].prompt === undefined) {
              fieldName = item;
            } else {
              fieldName = config[item].prompt;
            }
            return (
              <FormBuilder
                key={item}
                type={fType}
                field={field}
                fieldName={fieldName}
                value={toJson[item]}
                handleChange={handleChange}
              />
            );
          })}
          <StyledButton type="submit" onClick={() => handleSubmit()}>Submit form</StyledButton>
        </div>
      </PipelineFormStyled>
    );
  }
  return (
    <div>
      The system could not detect a manifest.json file with a &quot;
      {fName}
      &quot; property.
      <br />
      Please create the required file in the pipeline&apos;s repository or proceed with manual upload.
    </div>
  );
};

PipelineFormJson.propTypes = {
  config: PropTypes.shape({
    root: PropTypes.string,
  }).isRequired,
  onInputFormSubmit: PropTypes.func.isRequired,
  formType: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default PipelineFormJson;
