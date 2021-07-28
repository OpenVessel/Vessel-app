import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
//import {Link} from "react-router-dom";
import { useHistory } from "react-router-dom";

const Register = () => {

    const {store, actions} = useContext(Context);
    // const[csrf_token_passback, setCsrftoken] = useState("");
    const[username, setUsername] = useState("");
    const[email, setEmail] = useState("");
    const[password, setPassword] = useState("");
    const[confirmpassword, setConfirmpassword] = useState("");
    // const history = useHistory(); // using to redirect user to login page 

    //when the user registers 
    const handleClick = () => { 
        actions.registration( store.token_id, store.csrf_token, username, email, password, confirmpassword);
        // history.push("/login");
    };
    
    console.log(store.csrf_token)
    return (
        <div>
            <title>Register</title>
            <div> 
            {/* We have component controller component  */}
                <form action="" method="POST" name="register-form">
                {/* we can GET csrf from flask store local session */}
                <input id="token_id_passback" name="token_id_passback" type="hidden" value={store.token_id}/> 
                <input id="csrf_token_passback" name="csrf_token_passback" type="hidden" value={store.csrf_token}/> 
                <h4> Username </h4>
                <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
                <h4> Email </h4>
                <input type="text" placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                <h4> Password </h4>
                <input id="password" placeholder="password" required type="password" value={password} onChange={(e) => setPassword(e.target.value)}  /> 
                <h4> confirm password</h4>
                <input id="confirm_password" name="confirm_password" required type="password" placeholder="confirm_password" value={confirmpassword} onChange={(e) => setConfirmpassword(e.target.value)} />
                </form>
                <button onClick={handleClick}> Register </button>

            </div>
        </div>
    )
}

export default Register
