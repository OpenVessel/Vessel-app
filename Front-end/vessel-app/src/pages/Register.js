import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import "../css/login.css"
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
            <div className="container login-container register-container">
                <div className="login-form">
                    <div className="login-form-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-black.png'} alt="Logo" />
                        <h1 className="login-form-title">Create an account.</h1>
                        <p className="login-form-subtitle">Please enter your full legal name, matching your government ID.</p>
                        <div className="login-form-divider" />
                        <form>
                            <div className="login-form-controls">
                                <div className="login-form-control-input-container">
                                    <input className="login-form-control-input" type="text" id="fullName" placeholder="Full Name" />
                                    <label className="login-form-control-label" htmlFor="fullName">Full Name</label>
                                    <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <g opacity="0.5">
                                            <path d="M17.7083 22.1355H7.29159C3.4895 22.1355 1.302 19.948 1.302 16.1459V8.85423C1.302 5.05215 3.4895 2.86465 7.29159 2.86465H17.7083C21.5103 2.86465 23.6978 5.05215 23.6978 8.85423V16.1459C23.6978 19.948 21.5103 22.1355 17.7083 22.1355ZM7.29159 4.42715C4.31242 4.42715 2.8645 5.87506 2.8645 8.85423V16.1459C2.8645 19.1251 4.31242 20.573 7.29159 20.573H17.7083C20.6874 20.573 22.1353 19.1251 22.1353 16.1459V8.85423C22.1353 5.87506 20.6874 4.42715 17.7083 4.42715H7.29159Z" fill="#414859"/>
                                            <path d="M12.4997 13.4063C11.6247 13.4063 10.7393 13.1354 10.0622 12.5834L6.80181 9.9792C6.46848 9.70836 6.40598 9.21878 6.67682 8.88545C6.94765 8.55211 7.43723 8.48962 7.77057 8.76045L11.031 11.3646C11.8226 12 13.1664 12 13.9581 11.3646L17.2185 8.76045C17.5518 8.48962 18.0518 8.5417 18.3122 8.88545C18.5831 9.21878 18.531 9.71878 18.1872 9.9792L14.9268 12.5834C14.2601 13.1354 13.3747 13.4063 12.4997 13.4063Z" fill="#414859"/>
                                        </g>
                                    </svg>
                                </div>
                            </div>

                            <div className="login-form-controls">
                                <div className="login-form-control-input-container">
                                    <input className="login-form-control-input" type="text" id="emailAddress" placeholder="Enter email address" />
                                    <label className="login-form-control-label" htmlFor="emailAddress">Email address</label>
                                    <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <g opacity="0.5">
                                            <path d="M6.43752 23.698C6.33335 23.698 6.21877 23.6876 6.12502 23.6772L3.8646 23.3647C2.78127 23.2188 1.8021 22.2501 1.63544 21.1459L1.32294 18.8647C1.21877 18.1355 1.53127 17.1876 2.0521 16.6563L6.62502 12.0834C5.88544 9.12508 6.7396 6.00008 8.91669 3.84383C12.2917 0.479244 17.7813 0.468828 21.1667 3.84383C22.8021 5.47924 23.6979 7.65633 23.6979 9.96883C23.6979 12.2813 22.8021 14.4584 21.1667 16.0938C18.9792 18.2605 15.8646 19.1147 12.9271 18.3647L8.34377 22.9376C7.90627 23.3959 7.12502 23.698 6.43752 23.698ZM15.0313 2.87508C13.2084 2.87508 11.3959 3.56258 10.0104 4.94799C8.13544 6.81258 7.45835 9.54175 8.2396 12.0834C8.32294 12.3647 8.25002 12.6563 8.04169 12.8647L3.14585 17.7605C2.96877 17.9376 2.82294 18.3959 2.85419 18.6355L3.16669 20.9167C3.22919 21.3126 3.65627 21.7605 4.0521 21.8126L6.32294 22.1251C6.57294 22.1667 7.03127 22.0209 7.20835 21.8438L12.125 16.9376C12.3334 16.7292 12.6354 16.6667 12.9063 16.7501C15.4167 17.5417 18.1563 16.8647 20.0313 14.9897C21.3646 13.6563 22.1042 11.8647 22.1042 9.96883C22.1042 8.06258 21.3646 6.28133 20.0313 4.94799C18.6771 3.57299 16.8542 2.87508 15.0313 2.87508Z" fill="#414859"/>
                                            <path d="M9.57292 21.3959C9.375 21.3959 9.17708 21.323 9.02083 21.1667L6.625 18.7709C6.32292 18.4688 6.32292 17.9688 6.625 17.6667C6.92708 17.3646 7.42708 17.3646 7.72917 17.6667L10.125 20.0626C10.4271 20.3646 10.4271 20.8646 10.125 21.1667C9.96875 21.323 9.77083 21.3959 9.57292 21.3959Z" fill="#414859"/>
                                            <path d="M15.1042 12.2396C13.8126 12.2396 12.7605 11.1876 12.7605 9.89589C12.7605 8.60422 13.8126 7.55214 15.1042 7.55214C16.3959 7.55214 17.448 8.60422 17.448 9.89589C17.448 11.1876 16.3959 12.2396 15.1042 12.2396ZM15.1042 9.11464C14.6772 9.11464 14.323 9.46881 14.323 9.89589C14.323 10.323 14.6772 10.6771 15.1042 10.6771C15.5313 10.6771 15.8855 10.323 15.8855 9.89589C15.8855 9.46881 15.5313 9.11464 15.1042 9.11464Z" fill="#414859"/>
                                        </g>
                                    </svg>
                                </div>
                            </div>

                            <div className="login-form-controls">
                                <div className="login-form-control-input-container">
                                    <input className="login-form-control-input" type="text" id="password" aria-labelledby="password" placeholder="Enter Password" />
                                    <label className="login-form-control-label" id="password">Password</label>
                                    <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <g opacity="0.5">
                                            <path d="M6.43752 23.698C6.33335 23.698 6.21877 23.6876 6.12502 23.6772L3.8646 23.3647C2.78127 23.2188 1.8021 22.2501 1.63544 21.1459L1.32294 18.8647C1.21877 18.1355 1.53127 17.1876 2.0521 16.6563L6.62502 12.0834C5.88544 9.12508 6.7396 6.00008 8.91669 3.84383C12.2917 0.479244 17.7813 0.468828 21.1667 3.84383C22.8021 5.47924 23.6979 7.65633 23.6979 9.96883C23.6979 12.2813 22.8021 14.4584 21.1667 16.0938C18.9792 18.2605 15.8646 19.1147 12.9271 18.3647L8.34377 22.9376C7.90627 23.3959 7.12502 23.698 6.43752 23.698ZM15.0313 2.87508C13.2084 2.87508 11.3959 3.56258 10.0104 4.94799C8.13544 6.81258 7.45835 9.54175 8.2396 12.0834C8.32294 12.3647 8.25002 12.6563 8.04169 12.8647L3.14585 17.7605C2.96877 17.9376 2.82294 18.3959 2.85419 18.6355L3.16669 20.9167C3.22919 21.3126 3.65627 21.7605 4.0521 21.8126L6.32294 22.1251C6.57294 22.1667 7.03127 22.0209 7.20835 21.8438L12.125 16.9376C12.3334 16.7292 12.6354 16.6667 12.9063 16.7501C15.4167 17.5417 18.1563 16.8647 20.0313 14.9897C21.3646 13.6563 22.1042 11.8647 22.1042 9.96883C22.1042 8.06258 21.3646 6.28133 20.0313 4.94799C18.6771 3.57299 16.8542 2.87508 15.0313 2.87508Z" fill="#414859"/>
                                            <path d="M9.57292 21.3959C9.375 21.3959 9.17708 21.323 9.02083 21.1667L6.625 18.7709C6.32292 18.4688 6.32292 17.9688 6.625 17.6667C6.92708 17.3646 7.42708 17.3646 7.72917 17.6667L10.125 20.0626C10.4271 20.3646 10.4271 20.8646 10.125 21.1667C9.96875 21.323 9.77083 21.3959 9.57292 21.3959Z" fill="#414859"/>
                                            <path d="M15.1042 12.2396C13.8126 12.2396 12.7605 11.1876 12.7605 9.89589C12.7605 8.60422 13.8126 7.55214 15.1042 7.55214C16.3959 7.55214 17.448 8.60422 17.448 9.89589C17.448 11.1876 16.3959 12.2396 15.1042 12.2396ZM15.1042 9.11464C14.6772 9.11464 14.323 9.46881 14.323 9.89589C14.323 10.323 14.6772 10.6771 15.1042 10.6771C15.5313 10.6771 15.8855 10.323 15.8855 9.89589C15.8855 9.46881 15.5313 9.11464 15.1042 9.11464Z" fill="#414859"/>
                                        </g>
                                    </svg>
                                </div>
                                <div className="login-form-control-input-container">
                                    <input className="login-form-control-input" type="text" id="confirmPassword" aria-labelledby="password" placeholder="Confirm Password" style={{marginTop: "15px"}} />
                                    <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg" style={{transform: "translate(0, -20%)"}}>
                                        <g opacity="0.5">
                                            <path d="M6.43752 23.698C6.33335 23.698 6.21877 23.6876 6.12502 23.6772L3.8646 23.3647C2.78127 23.2188 1.8021 22.2501 1.63544 21.1459L1.32294 18.8647C1.21877 18.1355 1.53127 17.1876 2.0521 16.6563L6.62502 12.0834C5.88544 9.12508 6.7396 6.00008 8.91669 3.84383C12.2917 0.479244 17.7813 0.468828 21.1667 3.84383C22.8021 5.47924 23.6979 7.65633 23.6979 9.96883C23.6979 12.2813 22.8021 14.4584 21.1667 16.0938C18.9792 18.2605 15.8646 19.1147 12.9271 18.3647L8.34377 22.9376C7.90627 23.3959 7.12502 23.698 6.43752 23.698ZM15.0313 2.87508C13.2084 2.87508 11.3959 3.56258 10.0104 4.94799C8.13544 6.81258 7.45835 9.54175 8.2396 12.0834C8.32294 12.3647 8.25002 12.6563 8.04169 12.8647L3.14585 17.7605C2.96877 17.9376 2.82294 18.3959 2.85419 18.6355L3.16669 20.9167C3.22919 21.3126 3.65627 21.7605 4.0521 21.8126L6.32294 22.1251C6.57294 22.1667 7.03127 22.0209 7.20835 21.8438L12.125 16.9376C12.3334 16.7292 12.6354 16.6667 12.9063 16.7501C15.4167 17.5417 18.1563 16.8647 20.0313 14.9897C21.3646 13.6563 22.1042 11.8647 22.1042 9.96883C22.1042 8.06258 21.3646 6.28133 20.0313 4.94799C18.6771 3.57299 16.8542 2.87508 15.0313 2.87508Z" fill="#414859"/>
                                            <path d="M9.57292 21.3959C9.375 21.3959 9.17708 21.323 9.02083 21.1667L6.625 18.7709C6.32292 18.4688 6.32292 17.9688 6.625 17.6667C6.92708 17.3646 7.42708 17.3646 7.72917 17.6667L10.125 20.0626C10.4271 20.3646 10.4271 20.8646 10.125 21.1667C9.96875 21.323 9.77083 21.3959 9.57292 21.3959Z" fill="#414859"/>
                                            <path d="M15.1042 12.2396C13.8126 12.2396 12.7605 11.1876 12.7605 9.89589C12.7605 8.60422 13.8126 7.55214 15.1042 7.55214C16.3959 7.55214 17.448 8.60422 17.448 9.89589C17.448 11.1876 16.3959 12.2396 15.1042 12.2396ZM15.1042 9.11464C14.6772 9.11464 14.323 9.46881 14.323 9.89589C14.323 10.323 14.6772 10.6771 15.1042 10.6771C15.5313 10.6771 15.8855 10.323 15.8855 9.89589C15.8855 9.46881 15.5313 9.11464 15.1042 9.11464Z" fill="#414859"/>
                                        </g>
                                    </svg>
                                </div>
                            </div>

                            <div className="login-form-button">Sign Up</div>
                        </form>

                        <div className="login-form-link">
                            Already have an account? <Link to="/Login">Log in!</Link>
                        </div>
                    </div>
                </div>

                <div className="login-banner" style={{backgroundImage: "url(" + process.env.PUBLIC_URL + '/images/login-banner.png' + ")"}}>
                    <div className="login-banner-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-white.png'} alt="Logo"/>
                        <h1>Out-of-Pocket<br /> Insurance Premium.</h1>
                        <p>Make monthly payments of low-end $150 to pay off medical bills with small to large ducbuitles debt. To high-end premium of $300.</p>
                    </div>
                    <div className="login-banner-bottom-content">
                        <img src={process.env.PUBLIC_URL + '/images/login-rectangle.png'} alt="Rectangle"/>
                    </div>
                </div>
            </div>
            {/*<div className="container card_registeration">*/}
            {/*<title>Register</title>*/}
            {/*<div className="registration">*/}
            {/*    <div className="row outer-row ">*/}
            {/*    /!* We have component controller component  *!/*/}
            {/*    /!* <div className="one column">hello</div> *!/*/}
            {/*        <div className="eight columns card_registeration">*/}

            {/*        <img src={process.env.PUBLIC_URL + '/images/OVLogoBlack.svg'} alt="OpenVessel Logo" />*/}
            {/*            <h3> <b>Cover any out-pocket cost! </b> </h3>*/}
            {/*            <h6> OpenVessel let's you pay any medical bill for $100 a month as <b> invested*/}
            {/*            premium </b> that can be taken out in 6 months for the total of $600. </h6>*/}

            {/*            <b><p>Please enter your full legal name. Your legal name should match any form of government ID.</p></b>*/}

            {/*            {!isSubmitted ? <FormInput submitForm={submitForm}/> : <FormSuccess/> }*/}
            {/*            /!* well fix the button is simply not connected *!/*/}
            {/*            /!* <Link to="/contactInfo">  *!/*/}
            {/*            /!* </Link> *!/*/}

            {/*        </div>*/}
            {/*        <div className="four columns">*/}
            {/*        <SideBar title={title}> </SideBar>*/}
            {/*        </div>*/}
            {/*    </div> /!*   parent row *!/*/}
            {/*</div>*/}

            {/*    </div>*/}
            {/*    <div className="row row_background">*/}
            {/*    <p>*/}
            {/*    All paid premiums will be deposited into OpenVessel Financials LLC uitilize in a finanical instrustment collective collateral pool,*/}
            {/*    which is the finanical intrustment uitilized to pay your medical bill through the power of the blockchain*/}

            {/*    Emergency Medical Funds are not collateralized in the public pool or what's known as "collective premium collateral pool".*/}
            {/*    </p>*/}
            {/*    </div>*/}
        </div>
    );
}

export default Register
