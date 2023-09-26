import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import Login from "./routes/login/login";
import Home from "./routes/home/home";
import AllDeployments from "./routes/home/routes/all-deployments/all-deployments";
import CreateDeployment from "./routes/home/routes/create-deployment/create-deployment";
import EditDeployment from "./routes/home/routes/edit-deployment/edit-deployment";
import UserGuide from "./routes/home/routes/user-guide/user-guide";
import Analysis from "./routes/home/routes/analysis/analysis";

const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/",
    element: <Home />,
    children: [
      {
        path: "",
        element: <AllDeployments />
      },
      {
        path: "create-survey",
        element: <CreateDeployment />
      },
      {
        path: "edit-survey/:name",
        element: <EditDeployment />
      },
      {
        path: "user-guide",
        element: <UserGuide />
      },
      {
        path: "analysis",
        element: <Analysis />
      }
    ]
  }
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
