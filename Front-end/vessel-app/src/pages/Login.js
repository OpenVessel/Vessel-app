import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import {Link} from "react-router-dom";
import { useHistory } from "react-router";
import "../css/page_form.css";
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
            <div className="container page-form-container">
                <div className="page-form-banner" style={{backgroundImage: "url(" + process.env.PUBLIC_URL + '/images/login-banner2.png' + ")"}}>
                    <div className="page-form-banner-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-white.png'} alt="Logo"/>
                        <h1>Get started today.</h1>
                        <p>Bring to the table win-win survival strategies to ensure proactive domination without any particular corperate delays.</p>
                    </div>
                    <div className="page-form-banner-bottom-content">
                        <img src={process.env.PUBLIC_URL + '/images/login-rectangle.png'} alt="Rectangle"/>
                    </div>
                </div>

                <div className="page-form">
                    <div className="page-form-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-black.png'} alt="Logo" />
                        <h1 className="page-form-title">Welcome back.</h1>
                        <p className="page-form-subtitle">Log in to your account to access variable x and variable y!</p>
                        <div className="page-form-divider" />
                        <form>
                            <div className="page-form-controls">
                                <div className="page-form-control-input-container">
                                    <input className="page-form-control-input" type="text" id="emailAddress"/>
                                    <label className="page-form-control-label" htmlFor="emailAddress">Email address</label>
                                    <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <g opacity="0.5">
                                            <path d="M17.7083 22.1355H7.29159C3.4895 22.1355 1.302 19.948 1.302 16.1459V8.85423C1.302 5.05215 3.4895 2.86465 7.29159 2.86465H17.7083C21.5103 2.86465 23.6978 5.05215 23.6978 8.85423V16.1459C23.6978 19.948 21.5103 22.1355 17.7083 22.1355ZM7.29159 4.42715C4.31242 4.42715 2.8645 5.87506 2.8645 8.85423V16.1459C2.8645 19.1251 4.31242 20.573 7.29159 20.573H17.7083C20.6874 20.573 22.1353 19.1251 22.1353 16.1459V8.85423C22.1353 5.87506 20.6874 4.42715 17.7083 4.42715H7.29159Z" fill="#414859"/>
                                            <path d="M12.4997 13.4063C11.6247 13.4063 10.7393 13.1354 10.0622 12.5834L6.80181 9.9792C6.46848 9.70836 6.40598 9.21878 6.67682 8.88545C6.94765 8.55211 7.43723 8.48962 7.77057 8.76045L11.031 11.3646C11.8226 12 13.1664 12 13.9581 11.3646L17.2185 8.76045C17.5518 8.48962 18.0518 8.5417 18.3122 8.88545C18.5831 9.21878 18.531 9.71878 18.1872 9.9792L14.9268 12.5834C14.2601 13.1354 13.3747 13.4063 12.4997 13.4063Z" fill="#414859"/>
                                        </g>
                                    </svg>
                                </div>
                            </div>

                            <div className="page-form-controls">
                                <div className="page-form-control-input-container">
                                    <input className="page-form-control-input" type="text" id="password" aria-labelledby="password"/>
                                    <label className="page-form-control-label" id="password">Password</label>
                                    <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <g opacity="0.5">
                                            <path d="M6.43752 23.698C6.33335 23.698 6.21877 23.6876 6.12502 23.6772L3.8646 23.3647C2.78127 23.2188 1.8021 22.2501 1.63544 21.1459L1.32294 18.8647C1.21877 18.1355 1.53127 17.1876 2.0521 16.6563L6.62502 12.0834C5.88544 9.12508 6.7396 6.00008 8.91669 3.84383C12.2917 0.479244 17.7813 0.468828 21.1667 3.84383C22.8021 5.47924 23.6979 7.65633 23.6979 9.96883C23.6979 12.2813 22.8021 14.4584 21.1667 16.0938C18.9792 18.2605 15.8646 19.1147 12.9271 18.3647L8.34377 22.9376C7.90627 23.3959 7.12502 23.698 6.43752 23.698ZM15.0313 2.87508C13.2084 2.87508 11.3959 3.56258 10.0104 4.94799C8.13544 6.81258 7.45835 9.54175 8.2396 12.0834C8.32294 12.3647 8.25002 12.6563 8.04169 12.8647L3.14585 17.7605C2.96877 17.9376 2.82294 18.3959 2.85419 18.6355L3.16669 20.9167C3.22919 21.3126 3.65627 21.7605 4.0521 21.8126L6.32294 22.1251C6.57294 22.1667 7.03127 22.0209 7.20835 21.8438L12.125 16.9376C12.3334 16.7292 12.6354 16.6667 12.9063 16.7501C15.4167 17.5417 18.1563 16.8647 20.0313 14.9897C21.3646 13.6563 22.1042 11.8647 22.1042 9.96883C22.1042 8.06258 21.3646 6.28133 20.0313 4.94799C18.6771 3.57299 16.8542 2.87508 15.0313 2.87508Z" fill="#414859"/>
                                            <path d="M9.57292 21.3959C9.375 21.3959 9.17708 21.323 9.02083 21.1667L6.625 18.7709C6.32292 18.4688 6.32292 17.9688 6.625 17.6667C6.92708 17.3646 7.42708 17.3646 7.72917 17.6667L10.125 20.0626C10.4271 20.3646 10.4271 20.8646 10.125 21.1667C9.96875 21.323 9.77083 21.3959 9.57292 21.3959Z" fill="#414859"/>
                                            <path d="M15.1042 12.2396C13.8126 12.2396 12.7605 11.1876 12.7605 9.89589C12.7605 8.60422 13.8126 7.55214 15.1042 7.55214C16.3959 7.55214 17.448 8.60422 17.448 9.89589C17.448 11.1876 16.3959 12.2396 15.1042 12.2396ZM15.1042 9.11464C14.6772 9.11464 14.323 9.46881 14.323 9.89589C14.323 10.323 14.6772 10.6771 15.1042 10.6771C15.5313 10.6771 15.8855 10.323 15.8855 9.89589C15.8855 9.46881 15.5313 9.11464 15.1042 9.11464Z" fill="#414859"/>
                                        </g>
                                    </svg>
                                </div>
                            </div>

                            <div className="page-form-forgot-password">
                                <Link to="/">Forgot Password?</Link>
                            </div>

                            <div className="page-form-button">Log In</div>
                        </form>

                        <div className="page-form-link">
                            Don't have an account? <Link to="/Register">Register here.</Link>
                        </div>
                    </div>
                </div>
            </div>
            {/*<title>Login</title>*/}
            {/*{store.token && store.token !== "" && store.token !== undefined ? (*/}

            {/*    "You are logged in with this token " + store.token*/}

            {/*):(*/}
            {/*<div className="flex-container">*/}
            {/*<div className="flex-child card_login2">*/}
            {/*    <div className="flex-child rowLogin">*/}
            {/*    <div className="PositionImg">*/}
            {/*    <img src={process.env.PUBLIC_URL + '/images/OVLogoBlack.svg'} alt="OpenVessel Logo" />*/}
            {/*    </div>*/}
            {/*    <div className="flex-child TextBoxCenter">*/}

            {/*        <h1> Get Started today. </h1>*/}
            {/*        <p>Insurance is about spreading risk to the greater community*/}
            {/*        if it’s a business or if it’s someone’s Health, Blockchain has*/}
            {/*        a lot of spread and future growth but this doesn’t impact*/}
            {/*        our healthcare system or people’s lives</p>*/}
            {/*        </div>*/}
            {/*    </div>*/}
            {/*</div>*/}
            {/*<div className="flex-child card_login">*/}
            {/*    <div className="row flex-child rowLogin">*/}
            {/*    /!* We have component controller component  *!/*/}
            {/*    /!* src\images\OV_Logo_Black.svg *!/*/}

            {/*    <div className="headerleft" >*/}
            {/*    <img src={process.env.PUBLIC_URL + '/images/OVLogoBlack.svg'} alt="OpenVessel Logo" />*/}

            {/*    <div className="minibox">*/}
            {/*        <b> <h2 className="headerleft">Log In</h2> </b>*/}
            {/*        </div>*/}
            {/*        <p> Pay off medical debt, make emergrency funds with return on interest woth OpenVessel. </p>*/}
            {/*        <br></br>*/}
            {/*    </div>*/}
            {/*        <div className="minibox">*/}
            {/*            <label className="custom-field">*/}
            {/*                <div className="spacing">*/}
            {/*                /!* Username input *!/*/}
            {/*                <p> Username </p>*/}
            {/*                <input type="text"*/}
            {/*                placeholder="username"*/}
            {/*                value={username}*/}
            {/*                onChange={(e) => setUsername(e.target.value)} />*/}
            {/*                </div>*/}
            {/*                <div className="spacing">*/}
            {/*                /!* Password *!/*/}
            {/*                <p>Password</p>*/}
            {/*                <input type="password"*/}
            {/*                placeholder="password"*/}
            {/*                value={password}*/}
            {/*                onChange={(e) => setPassword(e.target.value)}  />*/}
            {/*                <p> Forget Password? </p>*/}
            {/*                </div>*/}

            {/*            </label>*/}

            {/*            <label className="custom-field">*/}
            {/*            <div className="spacing">*/}
            {/*            <button className="btn-main" onClick={handleClick}> Login </button>*/}
            {/*            <h1> {store.return_msg}</h1>*/}

            {/*            <Link to="/Register">*/}
            {/*            <p id="undertag"> Don't have an account?</p>*/}
            {/*            </Link>*/}
            {/*            </div>*/}
            {/*            </label>*/}
            {/*        </div>*/}
            {/*    </div>*/}
            {/*</div>*/}

            {/*</div>*/}
            {/*)}*/}
        </div>
    )
}

export default Login
