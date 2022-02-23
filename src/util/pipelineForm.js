import React from "react";
import styled from 'styled-components';
import {
  StyledButton,
} from 'styles/app';
// import {
//   uploadInputFile,
// } from 'actions/pipelines';
import MultiSelect from "react-multi-select-component";

const PipelineFormStyled = styled.div`
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: left;
`;

class PipelineForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidUpdate(prevProps, prevState) {
    if ((Object.keys(prevProps.data).length === 0) && (Object.keys(this.props.data).length !== 0)) {
      const data = this.props.data
      // get fileNames to specify what files are needed if input fields are not specified
      const fileNames = Object.keys(data)
      let fileNamesStr = ""
      fileNames.map((key)=>{
        fileNamesStr += (" " + key + ",")
      })
      // remove last comma from string
      const fileNamesString = fileNamesStr.slice(0, -1);
      const fileName = fileNames[0]
      const keys = Object.keys(data[fileName])
      let formState = {
        data: data,
        fileName: fileName,
        fileNamesString: fileNamesString,
        keys: keys
      }
      keys.map((key)=>{
        if (data[fileName][key]["type"] === "optionsMulti") {
          formState.[key] = [];
        } else {
          formState.[key] = null;
        }
      })
      this.setState(formState)
    }
  };

  toCsv = (e) => {
    let data = this.state
    const fileName = data.fileName
    // since state was dynamically created, accessing form data by
    // eliminating the ones we know exists
    delete data.data
    delete data.keys
    delete data.fileName

    let csvFormat = ""
    Object.keys(data).forEach(function(key) {
      // since the selected values are multiValue]
      let values = "";
      if (Array.isArray(data[key])) {
        data[key].map((x) => {
          values += x.value + " "
        });
      } else {
        values = data[key]
      }
      csvFormat += key + "," + values.trim() + "\n"
    })
    let arrayBuffer = new TextEncoder("utf-8").encode(csvFormat);
    this.props.onInputFormSubmit(e, arrayBuffer, fileName)
  };

  update = (field, event) => {
    this.setState({ [field]: event.target.value });
  };

  validatInput = (e, key) => {
    let value = e.target.value
    debugger;
  }

  optionsMulti = (key) => {
    let options = []
    this.state.data[this.state.fileName][key]["values"].map((option)=>{
      options.push({label: option, value: option})
    })
    return options
  };

  render() {
    if (this.state.keys) {
      return (
        <>
          <div>
          Required Files Are:
          { this.state.fileNamesString }
          </div>
          <PipelineFormStyled>
            <div className="pipelineForm row">
              {
                this.state.keys.map((key)=>{
                  return (
                    <div className="col-md-6">
                      <br />
                      <label for={ key }> { key }: </label>
                      { (this.state.data[this.state.fileName][key]["type"] === "optionsMulti")
                        ?
                        <>
                          <MultiSelect
                            options={ this.optionsMulti(key) }
                            value={ this.state[key] }
                            onChange={ (e) => this.setState({[key]: e}) }
                            labelledBy="Select"
                          />
                        </>
                        :
                        null
                      }
                      { (this.state.data[this.state.fileName][key]["type"] === "textField")
                        ?
                        <div className="form-group">
                          <input
                            className="form-control"
                            type="text"
                            onChange={ (e) => this.setState({[key]: e.target.value}) }
                          />
                        </div>
                        :
                        null
                      }
                      { (this.state.data[this.state.fileName][key]["type"] === "integerField")
                        ?
                        <div className="form-group">
                          <input
                            className="form-control"
                            type="number"
                            onChange={ (e) => this.setState({[key]: e.target.value}) }
                          />
                        </div>
                        :
                        null
                      }
                      { (this.state.data[this.state.fileName][key]["type"] === "dateField")
                        ?
                        <div className="form-group">
                          <input
                            className="form-control"
                            type="datetime-local"
                            onChange={ (e) => this.setState({[key]: e.target.value}) }
                          />
                        </div>
                        :
                        null
                      }
                    </div>
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
        </>
      );
    } else {
      return (
        <>
        </>
      )
    }
  }
}

export default PipelineForm;
