import React, {useState} from 'react'
import { Link } from "react-router-dom";
import SideBar from "../components/SideBar.js";
import FormSuccess from '../components/FormSuccess';
import FormInputIdVerification from '../components/FormInputIdVerification.js';


const IdVerification = () => {
    let title = 'Verification'
    function submitForm() {
        setIsSubmitted(true);
    }
    const [isSubmitted, setIsSubmitted] = useState(false);
     // using to redirect user to login page 
    // failling to redirect because both functions are async
    return (
        <div>
        <div className="container card_registeration">
            <title>{title}</title>
            <div className="registration"> 
                <div className="row outer-row ">
                {/* We have component controller component  */}
                {/* <div className="one column">hello</div> */}
                <div className="eight columns card_registeration">
                    
                <img src={process.env.PUBLIC_URL + '/images/OVLogoBlack.svg'} alt="OpenVessel Logo" />
                        <h4> <b> Verify Your Identity</b> </h4>
                        <h6> Please Provide <b> Contact Information </b> </h6>
                    <FormInputIdVerification/>
                    
                    {/* {!isSubmitted ? <FormInputIdVerification submitForm={submitForm}/> : <FormSuccess/> } */}
                </div>
                    <div className="four columns"> 
                    <SideBar title={title}> </SideBar>    
                    </div>
                
            </div>{/*   parent row */}
          
        </div>
    </div>
    <div className="row row_background"> 
    <p>
    All Social Secuirty Numbers are verified via authenticating.com SentiLink Corp. and Plaid
    </p>
    </div>

</div>
    )
}

export default IdVerification
