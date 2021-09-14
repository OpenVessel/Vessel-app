import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import {Link} from "react-router-dom";
import { useHistory } from "react-router";
// src\images\OV_Logo_Black.svg

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
    // this is the redirect push to another webpage after login is successfull
    if (store.token && store.token !== "" && store.token !== undefined) history.push("/Account");
    return (
        <div>
            <title>Login</title>
            {store.token && store.token !== "" && store.token !== undefined ? (
                
                "You are logged in with this token " + store.token 
            
            ):(
            <div className="flex-container"> 
            <div className="flex-child card_login2"> 
                <div className="flex-child rowLogin">
                <div className="PositionImg"> 
                <img src={process.env.PUBLIC_URL + '/images/OVLogoBlack.svg'} alt="OpenVessel Logo" />
                </div>
                <div className="flex-child TextBoxCenter"> 
                    
                    <h1> Get Started today. </h1>
                    <p>Insurance is about spreading risk to the greater community 
                    if it’s a business or if it’s someone’s Health, Blockchain has 
                    a lot of spread and future growth but this doesn’t impact 
                    our healthcare system or people’s lives</p> 
                    </div>
                </div>
            </div>
            <div className="flex-child card_login"> 
                <div className="row flex-child rowLogin"> 
                {/* We have component controller component  */}
                {/* src\images\OV_Logo_Black.svg */}
                
                <div className="headerleft" > 
                <img src={process.env.PUBLIC_URL + '/images/OVLogoBlack.svg'} alt="OpenVessel Logo" />
                    <b> <h2 className="headerleft">Log In</h2> </b> 
                    </div>
                    <p> Pay off medical debt, make emergrency funds with return on interest woth OpenVessel. </p>
                    <br></br>
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
