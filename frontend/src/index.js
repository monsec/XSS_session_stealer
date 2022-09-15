import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import "./output.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from './UserCreation/Login.jsx';
import Signup from './UserCreation/Signup.jsx';
import Feedback from './Feedback/Feedback.jsx';
import FeedbackAdmin from './Feedback/FeedbackAdmin.jsx';
import Comment from './Comment/Comment.jsx';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode >
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/signup" element={<Signup/>}/>
        <Route path="/user/feedback" element={<Feedback/>}/>
        <Route path="/admin/feedback" element={<FeedbackAdmin/>}/>
        <Route path="/admin/feedback/:id" element={<Comment/>}/>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

