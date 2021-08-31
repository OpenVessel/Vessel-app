import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
//import {Link} from "react-router-dom";
import { Link } from "react-router-dom";
import SideBar from "../components/SideBar.js";
import  { Redirect} from 'react-router-dom'
import FormSuccess from '../components/FormSuccess';
import { ErrorSharp } from '@material-ui/icons';
import FormInput from '../components/FormInput';

const Register = () => {
    const {store, actions} = useContext(Context);
    // const[csrf_token_passback, setCsrftoken] = useState("");
    // const[username, setUsername] = useState("");
    // const[firstname, setFirstname] = useState("");
    // const[lastname, setLastname] = useState("");
    // const[email, setEmail] = useState("");
    // const[password, setPassword] = useState("");
    // const[confirmpassword, setConfirmpassword] = useState("");

    let title = 'Register'
    // failling to redirect because both functions are async
    function submitForm() {
        setIsSubmitted(true);
    }
    const [isSubmitted, setIsSubmitted] = useState(false)

    
    console.log(store.csrf_token)
    return (
        <div>
            <div className="container card_registeration">
            <title>Register</title>
            <div className="registration"> 
                <div className="row outer-row ">
                {/* We have component controller component  */}
                {/* <div className="one column">hello</div> */}
                    <div className="eight columns card_registeration">
                    
                    <img className="image" src={process.env.PUBLIC_URL + '/images/OV_Logo_Black.png'} alt="OpenVessel2 Logo"/>
                        <h3> <b>Cover any out-pocket cost! </b> </h3>
                        <h6> OpenVessel let's you pay any medical bill for $100 a month as <b> invested
                        premium </b> that can be taken out in 6 months for the total of $600. </h6>

                        <b><p>Please enter your full legal name. Your legal name should match any form of government ID.</p></b>

                        {!isSubmitted ? <FormInput submitForm={submitForm}/> : <FormSuccess/> }
                        {/* well fix the button is simply not connected */}
                        {/* <Link to="/contactInfo">  */}
                        {/* </Link> */}

                    </div>
                    <div className="four columns"> 
                    <SideBar title={title}> </SideBar>    
                    </div>
                </div> {/*   parent row */}
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

export default Register
