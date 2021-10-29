import React, {useContext, useState} from 'react'
import {Context} from "../../appContext/UserContext"
import "../../css/page_form.css"
//import {Link} from "react-router-dom";
import { Link } from "react-router-dom";
import  { Redirect} from 'react-router-dom'
import FormSuccess from '../../components/FormSuccess';
import { ErrorSharp } from '@material-ui/icons';
import FormInput from '../../components/FormInput';

const Register = () => {
    const {store, actions} = useContext(Context);

    let title = 'Register'
    // failling to redirect because both functions are async
    function submitForm() {
        setIsSubmitted(true);
    }
    const [isSubmitted, setIsSubmitted] = useState(false)


    console.log(store.csrf_token)
    return (
        <div>
            <div className="container page-form-container register-container">
                <div className="page-form">
                    <div className="page-form-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-black.png'} alt="Logo" />
                        <h1 className="page-form-title">Create an account.</h1>
                        <p className="page-form-subtitle">Please enter your full legal name, matching your government ID.</p>
                        <div className="page-form-divider" />
                       
                        {!isSubmitted ? <FormInput submitForm={submitForm}/> : <FormSuccess/> }
                       
                    </div>
                </div>

                <div className="page-form-banner" style={{backgroundImage: "url(" + process.env.PUBLIC_URL + '/images/login-banner.png' + ")"}}>
                    <div className="page-form-banner-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-white.png'} alt="Logo"/>
                        <h1>Out-of-Pocket<br /> Insurance Premium.</h1>
                        <p>Make monthly payments of low-end $150 to pay off medical bills with small to large deductibles debt. To high-end premium of $300.</p>
                        
                        <h1> Premiums earn you Interest</h1>
                        
                        <p> After 6 months of paying Premiums you are allowed to 
                            withdraw your contributions in total but with contiuned contributions 
                            start building interest and increases with subsequent contributions.
                            </p>
                    </div>
                    <div className="page-form-banner-bottom-content">
                        <img src={process.env.PUBLIC_URL + '/images/login-rectangle.png'} alt="Rectangle"/>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Register
