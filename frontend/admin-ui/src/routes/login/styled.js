import styled from '@emotion/styled'
import { css } from '@emotion/react'


const pageWrapper = css`
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-content: center;
`

const leftLogoPane = css`
  display: flex;
  padding-right: 100px;
  flex-direction: column;
  justify-content: center;
  
  span:first-child {
    font-size: 3rem;
    color: #4f4f4f;
  }

  span:nth-child(2) {
    font-size: 1.9rem;
    color: #9c9c9c;
  }
`

const rightFormPane = css`
  display: flex;
  padding-left: 100px;
  border-left: 1px dashed #edebeb;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
`

const logos = css`
  display: flex;
  margin-top: 24px;
  gap: 24px;
  justify-content: center;
  img {
    width: 70px;
    filter: brightness(1.2) grayscale(0.8);
  }
`

const textBox = css`
  height: 36px;
  padding: 0 10px;
  font-size: 18px;
`

export const PageWrapper = styled.div`
  ${pageWrapper}
`

export const LeftLogoPane = styled.div`
  ${leftLogoPane}
`

export const RightFormPane = styled.div`
  ${rightFormPane}
`

export const Logos = styled.div`
  ${logos}
`

export const TextBox = styled.div`
  ${textBox}
`