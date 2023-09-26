import {css} from "@emotion/react";
import styled from "@emotion/styled";

const deploymentWrapper = css`
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: fit-content;
  
  label {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 16px;
    color: #9c9c9c;
    
    span {
      width: 150px;
    }
  }
`

export const DeploymentWrapper = styled.div`
  ${deploymentWrapper}
`