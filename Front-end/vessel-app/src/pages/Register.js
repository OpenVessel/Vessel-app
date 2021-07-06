import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
//import {Link} from "react-router-dom";

const Register = () => {

    const {store, actions} = useContext(Context);
    const[email, setEmail] = useState("");
    const[password, setPassword] = useState("");
    
    const handleClick = () => { 

        const opts = { 
            method:'POST',
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
                console.log("this came from the backend", data);
                sessionStorage.setItem("token", data.access_token);

            })

            .catch(error => {
                console.error("FETCH ERROR - LOGIN.JS ", error);
            })

    }
    
    return (
        <div>
            <title>Register</title>
            <div> 
            {/* We have component controller component  */}
                <input type="text" placeholder="email" value={email}onChange={(e) => setEmail(e.targert.value)} /> 
                <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.targert.value)}  />
                <button onClick={handleClick}> Register </button>

            </div>
        </div>
    )
}

export default Register
