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
            <div className="container card_login"> 
                <div className="row"> 
                {/* We have component controller component  */}
                <div>
                <div className="five column"> 
                <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
                </div>
                <div className="five column"> 
                <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)}  /> 
                </div>
                <button className="btn-main" onClick={handleClick}> Login </button>
                <h1> {store.return_msg}</h1>
                
                
                <Link to="/Register"> 
                <p> Don't have an account?</p>
                </Link>

                </div>
                </div>
            </div>
            )}
        </div>
    )
}

export default Login
