import React from "react";
import {LeftLogoPane, Logos, NavMenu, PageWrapper, RightFormPane} from "./styled";
import iriLogo from "../../assets/IRI_logo.jpg";
import columbiaLogo from "../../assets/columbia_logo.png";
import {NavLink, Outlet, useLocation} from "react-router-dom";
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Home = () => {

  const location = useLocation();
  const isActive = (path) => {
    console.log(location.pathname)
    return location.pathname === path;
  };


  return (
    <PageWrapper>
      <LeftLogoPane>
        <div className={'logo-text'}>
          <span>DESDR NOKi</span>
          <span>SURVEY YOUR WAY</span>
        </div>
        <NavMenu>
          <NavLink to={''}
                   className={() =>
                     isActive('/')
                       ? "active"
                       : ""
                   }>
            Surveys
          </NavLink>
          <NavLink to={'create-survey'}
                   className={() =>
                     isActive('/create-survey')
                       ? "active"
                       : ""
                   }>
            + New survey
          </NavLink>
          <NavLink to={'analysis'}
                   className={() =>
                     isActive('/analysis')
                       ? "active"
                       : ""
                   }>
            Analysis
          </NavLink>
          <NavLink to={'user-guide'}
                   className={() =>
                     isActive('/user-guide')
                       ? "active"
                       : ""
                   }>
            User guide
          </NavLink>
          <NavLink to={'login'}>
            Logout
          </NavLink>
        </NavMenu>
        <Logos>
          <img src={iriLogo}/>
          <img src={columbiaLogo}/>
        </Logos>
      </LeftLogoPane>
      <RightFormPane>
        <Outlet/>
      </RightFormPane>
      <ToastContainer/>
    </PageWrapper>
  )
}

export default Home