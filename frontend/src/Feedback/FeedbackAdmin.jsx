
import '../output.css';
import { useState, useEffect } from "react";

function FeedbackAdmin(){

  // require token
  const [token,setToken] = useState(localStorage.getItem("token"));
  const [comments,setComments] = useState([]);
  if(!token){
    window.location.href = "/login";
  }

  useEffect(() =>{
    
    fetch('http://localhost:9000/admin/feedback',{
      method:"GET",
      headers:{
        "Content-Type":"application/json",
        "Authorization":`Bearer ${token}`,
      },
    }).then(response =>{
      if (response.status !== 200){
        window.location.href = "/";
      }
      return response.json();
    })
    .then(data=>{
      setComments(data);
    })
    .catch(err =>{
      const mute = err;
    });
  },[]);

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
    .then(data=>{
      setComments(data);
    })
    .catch(err =>{
      const mute = err;
    })
  }

  return (
    <div className="text-center">
      <h1 className="mt-10 text-5xl PSP">Admin Panel</h1>
      <button className="bg-white drop-shadow-md mt-5 p-5 rounded text-xl font-bold hover:bg-gray-100" onClick={fetchComment}>Refresh</button>
      <div className="mt-10 text-left rounded w-1/4 mx-auto bg-white">
        {comments.map((comment) => (
          <div className="mt-5 font-bold text-lg p-4 hover:bg-gray-100 hover:text-sky-400">
            <a href={"/admin/feedback/"+comment.id}  >New Feedback! | {comment.created_date}</a>
          </div>
        ))}
      </div>
      
    </div>
    
  )
}

export default FeedbackAdmin;
