import React, {useEffect, useState} from "react";
import Deployment from "../../components/deployment/deployment";
import {useParams} from "react-router-dom";
import {axiosInstance} from "../../../../config/http";
import {get} from "lodash";
import {Button} from "../../../../common/styled";
import {EditDeploymentWrapper} from "../../styles/styled";
import {toast} from "react-toastify";
import {isValidJsonString} from "../../../../common/utils";

export default function EditDeployment() {
  const [deployment, setDeployment] = useState({})

  let {name} = useParams();
  useEffect(() => {
    axiosInstance.get('/deployment?deployment_name=' + name).then(response => {
      console.log(response)
      let deployment = get(response, 'data', [])
      let jsonScript = get(deployment, 'script', '')
      if (jsonScript) {
        jsonScript = JSON.parse(jsonScript)
        jsonScript = JSON.stringify(jsonScript, null, 4)
        deployment['script'] = jsonScript
      }
      setDeployment(deployment)
    }).catch(error => {
      console.log(error)
    })
  }, [name])

  const updateDeployment = () => {
    if (!isValidJsonString(deployment.script)) {
      toast.error("Syntax error in the script!")
      return
    }
    axiosInstance.put('/deployment', deployment).then(response => {
      if (get(response, 'data.msg', '') === 'success') {
        toast.success("Saved successfully!")
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
    {deployment && <Deployment isEdit deployment={deployment} setDeployment={setDeployment}/>}
    <Button onClick={updateDeployment}>Save changes</Button>
  </EditDeploymentWrapper>
}