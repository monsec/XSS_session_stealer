
import '../output.css';
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function Comment(){

  // require token
  const [token,setToken] = useState(localStorage.getItem("token"));
  if(!token){
    window.location.href = "/login";
  }

  // fetch all user comments
  const params = useParams();

  useEffect(() =>{
    //e.preventDefault();
    
    fetch(`http://localhost:9000/admin/feedback/${params.id}`,{
      method:"GET",
      headers:{
        "Content-Type":"application/json",
        "Authorization":`Bearer ${token}`,
      },
    }).then(response =>{
      if (response.status === 403){
        alert("Forbidden access");
        return;
        //window.location.href = "/";
      }
      return response.json();
    })
    .then(data=>{
      if (data.comment === undefined){
        document.getElementById("popup").style.display = "block";
        document.getElementById("prompt").innerText = "Not Found";
        document.getElementById("deleteButton").disabled = true;
        document.getElementById("deleteButton").classList.add("cursor-not-allowed");
      }
      else{
        document.getElementById("message").innerHTML = data.comment;
      }
    })
    .catch(err =>{
      const mute = err;
    });
  },[]);

  
  function deleteComment(){
    fetch(`http://localhost:9000/admin/feedback/${params.id}`,{
      method:"DELETE",
      headers:{
        "Content-Type":"application/json",
        "Authorization":`Bearer ${token}`,
      }
    }).then(response =>{
      if (response.status === 403){
        window.location.href="/";
      }
      return response.json();
    }).then(data=>{
      document.getElementById("popup").style.display="block";
      document.getElementById("prompt").innerText = "Comment deleted";
      window.setTimeout(function(){
        document.getElementById("prompt").innerText = "Redirecting...";
      },500)
      window.setTimeout(function(){
        window.location.href="/admin/feedback";
      },1000);
    }).catch(err => {
      const mute = err;
    })
  }
  
  return (
    <div className="text-center w-2/5 mx-auto">
      <h1 className="mt-10 text-5xl PSP">Admin Panel</h1>
      <div id="popup" className="mt-10 font-bold text-xl rounded drop-shadow-sm bg-white p-5 w-full hidden">
        <span id="prompt"></span>
      </div>
      <div className="mt-10 p-5 text-left rounded w-full mx-auto bg-white drop-shadow-md">
        <p id="message"className="text-xl break-all"></p>
      </div>
      <button id="deleteButton" className="mt-10 bg-white rounded p-5 hover:bg-gray-100 font-bold text-xl drop-shadow-md" onClick={deleteComment}>Delete</button>
      
    </div>
    
  )
}

export default Comment;
