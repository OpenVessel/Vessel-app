import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
//import {Link} from "react-router-dom";
import { Link } from "react-router-dom";
import SideBar from "../components/SideBar.js";
import  { Redirect} from 'react-router-dom'
import useForm from '../useForm'
import validate from '../validateInfo';
import FormSuccess from '../FormSuccess';
import { ErrorSharp } from '@material-ui/icons';


const Register = () => {
    const {store, actions} = useContext(Context);
    const [isSubmitted, setIsSubmitted] = useState(false)

    function submitForm() {
        setIsSubmitted(true);
    }

    const { handleChange, handleSubmit, values, errors } = useForm(
        submitForm,
        validate
      );

    // const[csrf_token_passback, setCsrftoken] = useState("");
    // const[username, setUsername] = useState("");
    // const[firstname, setFirstname] = useState("");
    // const[lastname, setLastname] = useState("");
    // const[email, setEmail] = useState("");
    // const[password, setPassword] = useState("");
    // const[confirmpassword, setConfirmpassword] = useState("");

    let title = 'Register'
    // failling to redirect because both functions are async
    const handleClick = () => { 
        // how to past data to handleClick? after validation?

        actions.registration( 
            store.token_id, 
            store.csrf_token, 
            values.firstname, 
            values.lastname, 
            values.username, 
            values.email,
            values.password, 
            values.confirmpassword);
    };
    
    console.log(store.csrf_token)
    console.log(isSubmitted)
    if(!isSubmitted) {
    return (
        <div>
            <div className="container card_registeration">
            <title>Register</title>
            <div className="registration"> 
                <div className="row outer-row ">
                {/* We have component controller component  */}
                {/* <div className="one column">hello</div> */}
                    <div className="eight columns card_registeration">
                    
                    <img src={process.env.PUBLIC_URL + '/images/OV_Logo_Black.png'} alt="OpenVessel2 Logo"/>
                        <h4> <b>Cover any out-pocket cost! </b> </h4>
                        <h6> OpenVessel let's you pay any medical bill for $100 a month as <b> invested
                        premium </b> that can be taken out in 6 months for the total of $600. </h6>

                        <b><p>Please enter your full legal name. Your legal name should match any form of government ID.</p></b>
                        <form action="" method="POST" name="register-form" onSubmit={handleSubmit}>
                        {/* we can GET csrf from flask store local session */}
                        <input id="token_id_passback" name="token_id_passback" type="hidden" value={store.token_id}/> 
                        <input id="csrf_token_passback" name="csrf_token_passback" type="hidden" value={store.csrf_token}/> 
                        <div className="row inner-row ">
                            <div className="four columns"> 
                                
                                {/* First Name Section */}
                                <input
                                type="text" 
                                name="firstname"
                                placeholder="First Name" 
                                className="form-input"
                                value={values.firstname} 
                                onChange={handleChange} 
                                />
                                {errors.firstname && <p>{errors.firstname}</p>}
                            </div>
                            <div className="four columns"> 
                                {/* Last Name */}
                                <input 
                                type="text" 
                                name="lastname"
                                className="form-input"
                                placeholder="Last Name" 
                                value={values.lastname} 
                                onChange={handleChange} />
                                {errors.lastname && <p>{errors.lastname}</p>}
                            </div>
                        </div>

                        <div className="row inner-row">
                            <div className="four columns"> 
                                {/* username input */}
                                <input 
                                type="text" 
                                name="username"
                                placeholder="username"
                                className="form-input" 
                                value={values.username} 
                                onChange={handleChange} 
                                />
                                {errors.username && <p>{errors.username}</p>}
                            </div>
                            <div className="four columns"> 
                                {/* Email Input */}
                                <input 
                                type="text" 
                                name="email"
                                placeholder="email" 
                                className="form-input"
                                value={values.email} 
                                onChange={handleChange}
                                />
                                {errors.email && <p>{errors.email}</p>}
                            </div>
                        </div>

                        <div className="row inner-row">
                            <div className="four columns"> 
                            {/* password input */}
                                <input id="password"
                                placeholder="password" 
                                required type="password" 
                                name="password"
                                className="form-input"
                                value={values.password} 
                                onChange={handleChange} 
                                /> 
                                {errors.password && <p>{errors.password}</p>}
                            </div>

                            <div className="four columns"> 
                            
                            {/* Confirm Input */}
                            <input 
                            id="confirm_password" 
                            name="confirmpassword" 
                            required type="password" 
                            className="form-input"
                            placeholder="Confirm Password" 
                            value={values.confirmpassword} 
                            onChange={handleChange}/>

                            {errors.confirmpassword && <p>{errors.confirmpassword}</p>}

                            </div>
                        </div>
                        </form>
                        <Link to="/contactInfo"> 
                        <button className="btn-main" onClick={handleClick} > Register </button>
                        </Link>

                        <a>  </a>

                    </div>
                    <div className="four columns"> 
                    <SideBar title={title}> </SideBar>    
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
        
        );
    }
    return <FormSuccess/>
}

export default Register
