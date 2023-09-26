import axios from "axios";
import {get} from "lodash";

export const axiosInstance = axios.create({
  // baseURL: 'http://localhost:5000' // for local testing
  baseURL: window.location.origin // for prod
});

axiosInstance.interceptors.request.use(
  function (config) {
    // Do something before request is sent
    console.log(config)
    const authToken = localStorage.getItem("auth");
    if (authToken) {
      config.headers = {...config.headers, Authorization: 'Bearer ' + authToken}
    }
    return config;
  },
  function (error) {
    // Do something with request error
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    console.log('oops: ', get(error, 'response.status'))
    if (get(error, 'response.status') === 401) {
      window.location.href = window.location.origin + '/login'
    }
    return Promise.reject(error);
  }
);