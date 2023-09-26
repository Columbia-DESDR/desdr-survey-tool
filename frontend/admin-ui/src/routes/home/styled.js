import {css} from "@emotion/react";
import styled from "@emotion/styled";

const pageWrapper = css`
  height: 100vh;
  width: 100vw;
  display: flex;
`

const leftLogoPane = css`
  display: flex;
  padding: 50px;
  flex-direction: column;
  justify-content: space-between;
  
  .logo-text {
    display: flex;
    flex-direction: column;
    min-width: 182px;
    
    span:first-child {
      font-size: 2rem;
      color: #4f4f4f;
    }

    span:nth-child(2) {
      font-size: 1.25rem;
      color: #9c9c9c;
    }
  }
`

const navMenu = css`
  display: flex;
  flex-direction: column;

  a {
    text-decoration: none;
    color: #c5c5c5;
    font-size: 1.2rem;
    font-weight: 400;
    margin-bottom: 24px;
    text-align: center;
    padding: 8px;

    &.active {
      color: #717171;
    }
    &:hover {
      color: #717171;
    }
  }
`

const logos = css`
  display: flex;
  gap: 24px;
  justify-content: center;
  img {
    width: 70px;
    filter: brightness(1.2) grayscale(0.8);
  }
`

const rightFormPane = css`
  display: flex;
  padding: 50px;
  overflow-y: scroll;
  flex-grow: 1;
  border-left: 1px dashed #b9b9b9;
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

export const NavMenu = styled.div`
  ${navMenu}
`
