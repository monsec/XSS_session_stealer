import "../output.css"
import { useState } from "react";


function Login(){
  let [username,setUsername] = useState("")
  let [password,setPassword] = useState("")
  
  const login = (e) => {
    if (username === "" | password === ""){
      return;
    }
    e.preventDefault();
    fetch("http://localhost:9000/user/login", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({
            "username": username,
            "password": password,
        })
    }).then(response => {
        if (response.status === 200) {
          document.getElementById("missing_values").style.display = "block";
          document.getElementById("message").innerText = "Logged in...";
          return response.json()
        }
        else if(response.status === 401){
          document.getElementById("missing_values").style.display = "block";
          document.getElementById("message").innerText = "Invalid username and/or password";
        }
    })
    .then(
      function (token) {
          localStorage.setItem("token", token["token"]);
          window.location.href = "/login"; // Need to redirect to feedback page
      }
    )
    .catch(err => { const mute = err })
  }
    return(
    <div>
      <h1 className='PSP text-5xl mt-5 text-center'>PAC-MAN</h1>
      <h2 className="PSP text-3xl mt-10 text-center">Login</h2>
      <section className='container mx-auto w-1/4 mt-10'>
        <div className="w-full bg-white py-3  text-center font-bold hidden" id="missing_values">
          <span id="message"></span>
        </div>
        <form className="w-full text-center">
            <input type="text" placeholder="username" required value={username} onChange={(e) => setUsername(e.target.value)} className="w-full mt-10 py-3 px-2 rounded drop-shadow-md"/>
            <input type="password" placeholder="password" required value={password} onChange={(e) => setPassword(e.target.value)} className="w-full mt-10 py-3 px-2 rounded drop-shadow-md"/>
            <input type="submit" name="submit" value="Log In" className="w-1/2 mt-10 py-3 px-2 rounded drop-shadow-md bg-white hover:bg-gray-100 hover:cursor-pointer" onClick={login}/>
        </form>
        <div className="text-center mt-10">
          <a href="/signup" className="text-xl font-bold text-sky-600 underline decoration-sky-400">Don't have an account?</a>
        </div>
      </section>
    </div>
    )
}

export default Login;
