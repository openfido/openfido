import React from 'react';
import ReactDOM from 'react-dom';
import styled from 'styled-components';
import {
  StyledModal,
  StyledButton,
  StyledText,
} from 'styles/app';
import {
  uploadInputFile,
} from 'actions/pipelines';

const PipelineFormStyled = styled.div`
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

class PipelineForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentWillMount() {
    const data = this.props.data
    const fileName = Object.keys(data)[0]
    const keys = Object.keys(data[fileName])
    let formState = {
      data: data,
      fileName: fileName,
      keys: keys
    }
    keys.map((key)=>{
      formState.[key] = null;
    })
    this.setState(formState)
  };

  toCsv = (e) => {
    let data = this.state
    const fileName = data.fileName
    // since state was dynamically created, accessing form data by
    // elminiating the ones we know exists
    delete data.data
    delete data.keys
    delete data.fileName

    let csvFormat = ""
    Object.keys(data).forEach(function(key) {
      csvFormat += key + "," + data[key] + "\n"
    })
    let arrayBuffer = new TextEncoder("utf-8").encode(csvFormat);
    this.props.onInputFormSubmit(e, arrayBuffer, fileName)
  };

  update = (field, event) => {
    this.setState({ [field]: event.target.value });
  };

  optionsMulti = (key) => {
    return (
      <select className="form-control" name={ key } id={ key } onChange={(e) => this.update(key , e)} multiple>
        {
          this.state.data[this.state.fileName][key]["values"].map((option)=>{
            return(
              <>
                <option value={ option }>
                  { option }
                </option>
              </>
            )
          })
        }
      </select>
    )
  };

  render() {
    if (this.state.keys) {
      return (
        <PipelineFormStyled>
          <div className="form-row pipelineForm">
            {
              this.state.keys.map((key)=>{
                return (
                  <>
                    <label for={ key }> { key }: </label>
                    { (this.state.data[this.state.fileName][key]["type"] === "optionsMulti")
                      ?
                      this.optionsMulti(key)
                      :
                      null
                    }
                    <br/>
                  </>
                )
              })
            }
          </div>
          <br />
          <StyledButton
            aria-label="Start Run button"
            size="middle"
            color="blue"
            width={108}
            onClick={ e => this.toCsv(e) }>
            Create Inputs
          </StyledButton>
          <br />
        </PipelineFormStyled>
      );
    }
  else {
    return (
      <>
      </>
    )
  }
  }
}

export default PipelineForm;
