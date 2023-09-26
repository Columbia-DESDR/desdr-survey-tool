import React, {useState} from "react";
import {axiosInstance} from "../../config/http";
import {get} from "lodash";
import {useNavigate} from "react-router-dom";
import {LeftLogoPane, Logos, PageWrapper, RightFormPane} from "./styled";
import iriLogo from "../../assets/IRI_logo.jpg";
import columbiaLogo from "../../assets/columbia_logo.png"
import {Button, InputBox} from "../../common/styled";

const Login = () => {
  const [creds, setCreds] = useState({username: '', password: ''})
  const navigate = useNavigate();

  // Navigation to this page results in logout
  localStorage.removeItem('auth')

  const login = async () => {
    try {
      const resp = await axiosInstance.post('/token', creds)
      if (get(resp, 'data.token', null)) {
        localStorage.setItem('auth', resp.data.token)
        navigate("/");
      }
      console.log(resp.data.token)
    } catch (e) {
      console.error("Failed auth: ", e)
    }

  }

  const credsChange = (e, type) => {
    const newCreds = {...creds}
    newCreds[type] = e.target.value
    setCreds(newCreds)
  }

  return (
    <PageWrapper>
      <LeftLogoPane>
        <span>DESDR NOKi</span>
        <span>SURVEY YOUR WAY</span>
        <Logos>
          <img src={iriLogo}/>
          <img src={columbiaLogo}/>
        </Logos>
      </LeftLogoPane>
      <RightFormPane>
        <InputBox placeholder={'Username'} type={'text'} onChange={(e) => credsChange(e, 'username')}
               value={creds.username}/>
        <InputBox placeholder={'Password'} type={'password'} onChange={(e) => credsChange(e, 'password')}
               value={creds.password}/>
        <Button onClick={login}>Login</Button>
      </RightFormPane>
    </PageWrapper>
  )
}

export default Login;
