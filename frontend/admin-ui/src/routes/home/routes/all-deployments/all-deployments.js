import React, {useEffect, useState} from "react";
import {axiosInstance} from "../../../../config/http";
import {get} from "lodash";
import {DeploymentCard, DeploymentList} from "./styled";
import {useNavigate} from "react-router-dom";

export default function AllDeployments() {
  const [deployments, setDeployments] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    axiosInstance.get('/deployment').then(response => {
      console.log(response)
      let deployments = get(response, 'data', [])
      setDeployments(deployments)
    }).catch(error => {
      console.log(error)
    })
  }, [])

  const gotoEditPage = (name) => {
    navigate('/edit-survey/' + name)
  }

  return (
    <DeploymentList>
      {
        deployments && deployments.length > 0 && deployments.map(d =>
          <DeploymentCard onClick={() => gotoEditPage(d.deployment_name)}>
            <div>
              <span>survey name:</span>
              <br />
              <span>{d.deployment_name}</span>
            </div>
            <div>
              <span>survey instance:</span>
              <br />
              <span>{d.instance_name}</span>
            </div>
            <div>
              <span>user start message:</span>
              <br />
              <span>{d.user_start_message}</span>
            </div>
            <div>
              <span>comments:</span>
              <br />
              <span>{d.comments}</span>
            </div>
          </DeploymentCard>
        )
      }
    </DeploymentList>
  )
}