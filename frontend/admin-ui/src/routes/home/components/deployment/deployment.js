import React, {useEffect} from "react";
import {get} from "lodash";
// import CodeEditor from '@uiw/react-textarea-code-editor';
import AceEditor from "react-ace";

import "ace-builds/src-noconflict/mode-json";
import "ace-builds/src-noconflict/theme-monokai";
import "ace-builds/src-noconflict/ext-language_tools";
import {DeploymentWrapper} from "./styled";
import {InputBox} from "../../../../common/styled";


const Deployment = ({deployment, setDeployment, isEdit}) => {
  const updateDeployment = (newVal, property) => {
    const newDeployment = {...deployment}
    newDeployment[property] = newVal
    setDeployment(newDeployment)
  }

  return (
    <DeploymentWrapper>
      <label>
        <span>Survey name:</span>
        <InputBox disabled={isEdit} type={'text'} placeholder={'Enter survey name'} value={deployment.deployment_name}
                  height={24} fontSize={14}
                  onChange={(e) => updateDeployment(e.target.value, 'deployment_name')}/>
      </label>
      <label>
        <span>Instance name:</span>
        <InputBox type={'text'} placeholder={'Enter instance name'} value={deployment.instance_name}
                  height={24} fontSize={14}
                  onChange={(e) => updateDeployment(e.target.value, 'instance_name')}/>
      </label>
      <label>
        <span>Start message:</span>
        <InputBox type={'text'} placeholder={'Enter start message'} value={deployment.user_start_message}
                  height={24} fontSize={14}
                  onChange={(e) => updateDeployment(e.target.value, 'user_start_message')}/>
      </label>
      <label>
        <span>Comments:</span>
        <InputBox type={'text'} placeholder={'Add comments'} value={deployment.comments}
                  height={24} fontSize={14}
                  onChange={(e) => updateDeployment(e.target.value, 'comments')}/>
      </label>
      <label>
        Script:
      </label>
      <AceEditor
        mode="json"
        theme="monokai"
        onChange={(nv) => updateDeployment(nv, 'script')}
        name="deployment"
        value={deployment.script}
        fontSize={14}
        height={'600px'}
        width={'725px'}
        showPrintMargin={true}
        showGutter={true}
        highlightActiveLine={true}
        setOptions={{
          enableBasicAutocompletion: true,
          enableLiveAutocompletion: true,
          enableSnippets: false,
          showLineNumbers: true,
          tabSize: 2,
          useWorker: false,
        }}
      />
    </DeploymentWrapper>
  )
}

export default Deployment