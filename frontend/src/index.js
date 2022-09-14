import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import "./output.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from './UserCreation/Login';
import Signup from './UserCreation/Signup';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode >
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/signup" element={<Signup/>}/>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

