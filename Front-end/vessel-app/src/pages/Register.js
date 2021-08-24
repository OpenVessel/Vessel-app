import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
//import {Link} from "react-router-dom";
import { Link } from "react-router-dom";
import SideBar from "../components/SideBar.js";
import  { Redirect} from 'react-router-dom'
import { useHistory } from "react-router-dom";

const Register = () => {

    const {store, actions} = useContext(Context);
    // const[csrf_token_passback, setCsrftoken] = useState("");
    const[username, setUsername] = useState("");
    const[firstname, setFirstname] = useState("");
    const[lastname, setLastname] = useState("");
    const[email, setEmail] = useState("");
    const[password, setPassword] = useState("");
    const[confirmpassword, setConfirmpassword] = useState("");
    // const history = useHistory(); // using to redirect user to login page 
    const history = useHistory();
    const title = 'Register'
    // failling to redirect because both functions are async
    const handleClick = () => { 
        actions.registration( store.token_id, store.csrf_token, firstname, lastname, username, email, password, confirmpassword);

    };
    
    console.log(store.csrf_token)
    return (
        <div>
            <div className="container card_registeration" >
            <title>Register</title>

             
            <div className="registration"> 
                <div className="row outer-row ">
                {/* We have component controller component  */}
                {/* <div className="one column">hello</div> */}
                    <div className="eight columns card_registeration">\
                    
                    <img src={process.env.PUBLIC_URL + '/images/OV_Logo_Black.png'} alt="OpenVessel2 Logo"/>
                        <h4> <b>Cover any out-pocket cost! </b> </h4>
                        <h6> OpenVessel let's you pay any medical bill for $100 a month as <b> invested
                        premium </b> that can be taken out in 6 months for the total of $600. </h6>

                        <b><p>Please enter your full legal name. Your legal name should match any form of government ID.</p></b>
                        <form action="" method="POST" name="register-form">
                        {/* we can GET csrf from flask store local session */}
                        <input id="token_id_passback" name="token_id_passback" type="hidden" value={store.token_id}/> 
                        <input id="csrf_token_passback" name="csrf_token_passback" type="hidden" value={store.csrf_token}/> 
                        <div className="row inner-row ">
                            <div className="four columns"> 
                                
                                <input type="text" placeholder="First Name" value={firstname} onChange={(e) => setFirstname(e.target.value)} />
                            </div>
                            <div className="four columns"> 
                                <input type="text" placeholder="Last Name" value={lastname} onChange={(e) => setLastname(e.target.value)} />
                            </div>
                        </div>

                        <div className="row inner-row">
                            <div className="four columns"> 
                                
                            <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
                            </div>
                            <div className="four columns"> 
                            <input type="text" placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                            </div>
                        </div>

                        <div className="row inner-row">
                            <div className="four columns"> 
                                
                            <input id="password" placeholder="password" required type="password" value={password} onChange={(e) => setPassword(e.target.value)}  /> 
                            </div>
                            <div className="four columns"> 
                            <input id="confirm_password" name="confirm_password" required type="password" placeholder="Confirm Password" value={confirmpassword} onChange={(e) => setConfirmpassword(e.target.value)} />>
                            </div>
                        </div>
                        </form>
                        <Link to="/contactInfo"> 
                        <button className="btn-main" onClick={handleClick} > Register </button>
                        </Link>

                        <a>  </a>

                    </div>
                    <div className="four columns"> 
                    <SideBar props={title}> </SideBar>    
                    </div>
                </div> {/*   parent row */}
                <h1> {store.return_msg}</h1>
            </div>

                </div>
                <div className="row row_background"> 
                <p>
                All paid premiums will be despoited into collective collateral pool,
                which is the finanical intrustment uitilized to pay your medical bill through the power of the blockchain 
                </p>
                </div>

        </div>
    )
}

export default Register
