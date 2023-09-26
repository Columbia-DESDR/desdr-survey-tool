import {css} from "@emotion/react";
import styled from "@emotion/styled";

const inputBox = props => css`
  height: ${props.height ? props.height : 36}px;
  padding: 0 10px;
  font-size:  ${props.fontSize ? props.fontSize : 18}px;
  color: #4c4c4c;
`


export const InputBox = styled.input`
  ${inputBox}
`

const button = css`
  width: fit-content;
  padding: 10px;
  height: 40px;
  background: #4f4f4f;
  color: white;
  border: 0;
  cursor: pointer;
  font-size: 15px;
  text-transform: uppercase;
`

export const Button = styled.button`
  ${button}
`