
import '../output.css';
import { useState } from "react";

function FeedbackAdmin(){

  // require token
  const [token,setToken] = useState(localStorage.getItem("token"));
  if(!token){
    window.location.href = "/login";
  }

  // fetch all user comments
  const fetchComment = (e) =>{
    e.preventDefault();
    
    fetch("http://localhost:9000/admin/feedback",{
      method:"GET",
      headers:{
        "Content-Type":"application/json",
        "Authorization":`Bearer ${token}`
      },
    }).then(response =>{
      if (response.status === 403){
        alert("Forbidden access")
        //window.location.href = "/";
      }
      return response.json();
    })
    .then(comments =>{
      console.log(comments);
    })
  }

  return (
    <div>
      <h1>Admin Panel</h1>
      <button onClick={fetchComment}>Refresh</button>
    </div>
    
  )
}

export default FeedbackAdmin;
