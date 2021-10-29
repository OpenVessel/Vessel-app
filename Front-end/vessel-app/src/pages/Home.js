import React, { useEffect,useContext} from 'react';
import {Context} from "../appContext/UserContext"
import {Link} from "react-router-dom";
import "../css/page_form.css";
import HomeNavBar from '../components/Homepage/HomeNavBar';
function Home() {
    const{store, actions } = useContext(Context);   
    useEffect(()=> {

        if(store.token && store.token !== "" && store.token !== undefined) actions.getMessage();

    }, [store.token]);
    //alt='OpenVessel Logo' style='margin:2%' height='10%' width='50%'
    //https://daveceddia.com/react-image-tag/
    // let imageName = require("/vessel-app/public/OpenVessel_Logo.png")
    // const {value, setValue} = useContext(TestContext);

    return (
        <div>
        {/* Navbar */}
        <HomeNavBar/>
            <div className="Homepage">
            <img src={process.env.PUBLIC_URL + '/images/OpenVessel_Logo.png'} alt="OpenVessel Logo"/>
            
            {/* tagline */}
            <div className="tagline"> 
            <h1> Health Insurance funded by the blockchain. </h1>
            </div>
            <div className="box"> 
            {/* className="btn btn-main" */}
                <div className="front-page"> 
                <Link className="page-form-button" to="/login" >Login</Link>
                <Link  className="page-form-button" to="/register" >Register</Link>
                </div>
            </div>
            
    <div className="front-page-section"> 
    

    <h2> Health Insurance policy created and funded through Smarts Contracts</h2>

    <p> Insuree, User, Customer, Investor, can interact with
        OpenVessel's Health Insurance Smart Contract Policy. 
    </p>

    <p> OpenVessel Smart Contract uilitze's Smart Contract technology stack 
    from Jubilant Market. Jubilant Market allows us to access liquilty from 
    the blockchain to pay for medical claims submitted to our system 
    to create Submitted Claim to a Deployed Smart Contract on the blockchain. </p>

    <p> Jubilant Markert is an Smart Contract created to interact with various blockchain 
    ecosystem to leverage assets to generate yield farming, price checking, and lending protocols 
    to cover the cost of Insurance Claims</p>

    <p>When an Hospital System, Medical Billing Company, User, Delegate, Insuree, 
    pays into the Insurance Smart Contract or uses our API, we on ramp your fiat
    currency into crpyto assets to pay for periumns for of Insurance Policy and 
    Off ramp the currency to pay for the insurance claim. </p> 

            </div>    

            </div>
        </div>
    )
}

export default Home
