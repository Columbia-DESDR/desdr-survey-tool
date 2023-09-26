import React, {useState} from "react";
import Deployment from "../../components/deployment/deployment";
import {Button} from "../../../../common/styled";
import {EditDeploymentWrapper} from "../../styles/styled";
import jsonScript from './sample_script.json'
import {axiosInstance} from "../../../../config/http";
import {useNavigate} from "react-router-dom";
import {toast} from 'react-toastify';
import {get} from "lodash";
import {isValidJsonString} from "../../../../common/utils";

export default function CreateDeployment() {
  const navigate = useNavigate()
  const sampleDeployment = {
    deployment_name: '',
    instance_name: '',
    user_start_message: '',
    comments: '',
    script: JSON.stringify(jsonScript, null, 4),
  }

  const [deployment, setDeployment] = useState(sampleDeployment)

  const createDeployment = () => {
    if (!isValidJsonString(deployment.script)) {
      toast.error("Syntax error in the script!")
      return
    }
    axiosInstance.post('/deployment', deployment).then(response => {
      if (get(response, 'data.msg', '') === 'success') {
        toast.success("Survey created!")
        navigate('/')
      } else if (get(response, 'data.error')) {
        toast.error("Failed! " + get(response, 'data.error'))
      } else {
        toast.error("Failed! Please contact the dev team.")
      }
    }).catch(error => {
      console.error(error)
      toast.error("Failed! Please contact the dev team.")
    })
  }

  return <EditDeploymentWrapper>
    {deployment && <Deployment deployment={deployment} setDeployment={setDeployment}/>}
    <Button onClick={createDeployment}>Create survey</Button>
  </EditDeploymentWrapper>
}