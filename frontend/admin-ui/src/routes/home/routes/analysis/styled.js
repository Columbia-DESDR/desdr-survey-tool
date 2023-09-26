import {css} from "@emotion/react";
import styled from "@emotion/styled";

const wrapper = css`
  width: 100%;
`
export const Wrapper = styled.div`
  ${wrapper}
`

const dropdownUl = props => css`
  margin: 2px 0;
  position: absolute;
  min-width: 200px;
  max-height: 400px;
  overflow-y: scroll;
  background-color: white;
  border: 1px solid #b9b9b9;
  display: ${props.isOpen ? 'block' : 'none'};
  padding-inline-start: 0;
`

export const DropdownUl = styled.ul`
  ${dropdownUl}
`

const dropdownLi = props => css`
  list-style-type: none;
  padding: 7px;
  border-bottom: 1px solid #b9b9b9;

  &:hover {
    background-color: #cecece;
    cursor: pointer;
    color: #000000;
  }
`

export const DropdownLi = styled.li`
  ${dropdownLi}
`

const dropdown = css`
  border: 1px solid #b9b9b9;
  padding: 7px;
  cursor: pointer;
`
export const Dropdown = styled.div`
  ${dropdown}
`

const content = css`
  border: 1px dashed #b9b9b9;
  margin-top: 24px;
  width: 100%;
  padding: 12px;
  
  table {
    border-collapse: collapse;
    th {
      border: 1px solid black;
      padding: 8px;
      text-align: left;
      background-color: #f2f2f2;
    }
    td {
      border: 1px solid black;
      padding: 8px;
    }
  }
`
export const Content = styled.div`
  ${content}
`