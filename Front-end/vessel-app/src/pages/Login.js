import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import {Link} from "react-router-dom";
import { useHistory } from "react-router";

const Login = () => {

    const{store, actions } = useContext(Context);
    const[email, setEmail] = useState("");
    const[password, setPassword] = useState("");
    const history = useHistory();
    
    const token = sessionStorage.getItem("token");
    console.log("this is your token", store.token)

    const handleClick = () => { 
    actions.login(email, password);
    };
    
    if (store.token && store.token !== "" && store.token != undefined) history.push("/");
    return (
        <div>
            <title>Login</title>
            {(store.token && store.token !== "") ? "You are logged in with this token " + token :
            
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
