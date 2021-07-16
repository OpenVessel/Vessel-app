import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
//import {Link} from "react-router-dom";
import { useHistory } from "react-router-dom";

const Register = () => {

    const {store, actions} = useContext(Context);
    const[csrf_token, setCsrftoken] = useState("");
    const[username, setUsername] = useState("");
    const[email, setEmail] = useState("");
    const[password, setPassword] = useState("");
    const[confirmpassword, setConfirmpassword] = useState("");
    const history = useHistory(); // using to redirect user to login page 

    //when the user registers 
    const handleClick = () => { 
        actions.registration(username, email, password, confirmpassword);
        history.push("/login");
    };
    
    return (
        <div>
            <title>Register</title>
            <div> 
            {/* We have component controller component  */}
                <form action="" name="register-form">
                {/* we can GET csrf from flask store local session */}
                <input id="csrf_token" name="csrf_token" type="hidden" value={csrf_token} onSubmit={setCsrftoken()}/> 
                <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
                <input type="text" placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)}  /> 
                <input type="text" placeholder="confirm password" value={confirmpassword} onChange={(e) => setConfirmpassword(e.target.value)} />
                </form>
                <button onClick={handleClick}> Register </button>

            </div>
        </div>
    )
}

export default Register
