import '../output.css';
import { useState } from "react";

function Feedback(){

  // require token
  const [token,setToken] = useState(localStorage.getItem("token"));
  if(!token){
    window.location.href = "/login";
  }

  // send comment message
  let [comment,setComment] = useState("")
  const sendComment = (e) =>{
    e.preventDefault();
    
    if (comment === ""){
      document.getElementById("missing_value").style.display = "block";
      document.getElementById("message").innerText = "Please put some text"
      return;
    }
    fetch("http://localhost:9000/user/feedback",{
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        "Authorization":`Bearer ${token}`
      },
      body: JSON.stringify({
        "comment":comment,
      })
    }).then(response =>{
      if(response.status === 201){
        document.getElementById("missing_value").style.display = "block";
        document.getElementById("message").innerText = "Comment Sent!";
        window.setTimeout(function(){
          document.getElementById("missing_value").style.display = "none";
        },1500)
        return;
      }
      else{
        document.getElementById("missing_value").style.display = "block";
        document.getElementById("message").innerText = "Something went wrong";
        return;
      }
    })
  }

  return (
    <div>
      <h1 className="mt-10 PSP text-5xl text-center">Admin Feedback!</h1> 
      <section className="text-center mx-auto w-1/2 mt-10">
        <div className="w-full bg-white py-3 text-center font-bold hidden drop-shadow-md rounded" id="missing_value">
          <span id="message"></span>
        </div>
        <form className="mt-10">
          <textarea required value={comment} onChange={(e) => setComment(e.target.value)}  placeholder="comment here..." className="rounded p-5 w-full drop-shadow-md"/>
          <button className="w-1/2 mt-10 py-3 px-2 rounded drop-shadow-md bg-white hover:bg-gray-100 font-bold text-xl hover:cursor-pointer" onClick={sendComment} >SEND</button>
        </form>
      </section>
    </div>
  )
}

export default Feedback;
