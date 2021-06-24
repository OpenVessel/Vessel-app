import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import {Link} from "react-router-dom";

const Login = () => {

    const{ store, actions } = useContext(Context);
    const[email, setEmail] = useState("");
    const[password, setPassword] = useState("");
    const token = sessionStorage.getItem("token");
    console.log("this is your token", token)
    const handleClick = () => { 

        const opts = { 
            method:'POST',
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                "email":email,
                "password": password 
            })
        }

        fetch('http://127.0.0.1:5000/api/token', opts)
            .then(resp => { 
                if(resp.status === 200) return resp.json();
                else alert("Error 200 Login.js")
            }) 
            .then(data => {
                //localstorage persenitdata
                // sessionStorage 
                console.log("this came from the backend", data)
                sessionStorage.setItem("token", data.access_token)
            })
            .catch(error => {
                console.error("FETCH ERROR - LOGIN.JS ", error);
            })

    }
    
    return (
        <div>
            <title>Login</title>
            {(token && token!=undefined) ? "You are logged in with this token" + token :
            <div> 
            {/* We have component controller component  */}
            
                <input type="text" placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)}  /> 
                <button onClick={handleClick}> Login </button>

                <p> Don't have an account?</p>
                <Link to="/Account"> Account </Link>
            </div>
            }
        </div>
    )
}

export default Login
