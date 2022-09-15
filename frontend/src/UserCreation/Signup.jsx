import "../output.css"
import { useState } from "react";


function Login(){
  let [username,setUsername] = useState("")
  let [password,setPassword] = useState("")
  
  const signup = (e) => {
    e.preventDefault();
    fetch("http://localhost:9000/user/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({
            "username": username,
            "password": password,
        })
    }).then(response => {
        if (response.status === 201) {
            window.location.href = "/login";
        }
        else if (response.status === 409){
          document.getElementById("missing_values").style.display = "block";
          document.getElementById("message").innerText = "Username taken";
        }
        else if (response.status === 400){
          document.getElementById("missing_values").style.display = "block";
          document.getElementById("message").innerText = "Something went wrong";
        }
    })
    .catch(function (e) {
        console.log(e);
    })
  }
    return(
    <div>
      <h1 className='PSP text-5xl mt-5 text-center'>PAC-MAN</h1>
      <h2 className="PSP text-3xl mt-10 text-center">Sign Up</h2>
      <section className='container mx-auto w-1/4 mt-10'>
        <div className="w-full bg-white py-3  text-center font-bold hidden" id="missing_values">
          <span id="message"></span>
        </div>
        <form className="w-full text-center">
            <input type="text" placeholder="username" required value={username} onChange={(e) => setUsername(e.target.value)} className="w-full mt-10 py-3 px-2 rounded drop-shadow-md"/>
            <input type="password" placeholder="password" required value={password} onChange={(e) => setPassword(e.target.value)} className="w-full mt-10 py-3 px-2 rounded drop-shadow-md"/>
            <input type="submit" value="Sign up" name="submit" className="w-1/2 mt-10 py-3 px-2 rounded drop-shadow-md bg-white hover:bg-gray-100 hover:cursor-pointer" onClick={signup}/>
        </form>
        <div className="text-center mt-10">
          <a href="/login" className="text-xl font-bold text-sky-600 underline decoration-sky-400">Already got an account?</a>
        </div>
      </section>
    </div>
    )
}

export default Login;
