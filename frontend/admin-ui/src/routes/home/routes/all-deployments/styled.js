import {css} from "@emotion/react";
import styled from "@emotion/styled";

const deploymentList = css`
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: fit-content;
`

const deploymentCard = css`
  display: flex;
  padding: 24px;
  gap: 36px;
  border: 1px dashed #c9c9c9;
  align-items: center;
  
  &:hover {
    border: 1px solid #9e9e9e;
    cursor: pointer;
  }

  div {
    min-width: 200px;
    span {
      &:first-child {
        color: #a8a8a8;
      }

      &:nth-child(3) {
        color: #696969;
      }
    }
  }
`

export const DeploymentList = styled.div`
  ${deploymentList}
`

export const DeploymentCard = styled.div`
  ${deploymentCard}
`