import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import {Link} from "react-router-dom";
import { useHistory } from "react-router";

const Login = () => {

    const{store, actions } = useContext(Context); //re-render when token is recevied
    const[username, setUsername] = useState("");
    const[password, setPassword] = useState("");
    const history = useHistory();
    
    const token = sessionStorage.getItem("token");
    console.log("this is your token", store.token)

    // async and react? // so when actions.login returns with true we redirect to account page
    const handleClick = () => { 
        console.log("loggin")
        actions.login(username, password);
    };
    
    if (store.token && store.token !== "" && store.token !== undefined) history.push("/Account");
    return (
        <div>
            <title>Login</title>
            {store.token && store.token !== "" && store.token != undefined ? (
                
                "You are logged in with this token " + store.token 
            
            ):(
            <div> 
                {/* We have component controller component  */}
                <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
                <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)}  /> 
                <button onClick={handleClick}> Login </button>
                <h1> {store.return_msg}</h1>
                <p> Don't have an account?</p>
                <Link to="/Account"> Account </Link>
            </div>
            )}
        </div>
    )
}

export default Login
