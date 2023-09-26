import {css} from "@emotion/react";
import styled from "@emotion/styled";

const wrapper = css`
  color: #575757;
  font-size: 16px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: fit-content;

  li {
    margin: 5px 0;
  }
`

export const Wrapper = styled.div`
  ${wrapper}
`

const pageHeading = css`
  font-size: 36px;
`

export const PageHeading = styled.div`
  ${pageHeading}
`

const section = css`
  display: flex;
  flex-direction: column;
  gap: 18px;
`

export const Section = styled.div`
  ${section}
`

const code = css`
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New', monospace;
`

export const Code = styled.pre`
  ${code}
`

const subSection = css`
  display: flex;
  flex-direction: column;
  gap: 18px;

  ul {
    li {
      margin-bottom: 12px;
    }
  }
`

export const SubSection = styled.div`
  ${subSection}
`