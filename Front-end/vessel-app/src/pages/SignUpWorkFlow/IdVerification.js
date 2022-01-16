import React, {useState} from 'react';
import "../../css/page_form.css";
import FormInputIdVerification from '../../components/FormInputIdVerification.js';


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
            <div className="container page-form-container">
                <div className="page-form-banner" style={{backgroundImage: "url(" + process.env.PUBLIC_URL + '/images/login-banner.png' + ")"}}>
                    <div className="page-form-banner-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-white.png'} alt="Logo"/>
                        <h1>Welcome!</h1>
                        <p>Make monthly payments of low-end $150 to pay off any
                            medical bills with small to large ducbuitles debt.
                            To high-end of $300.</p>
                    </div>
                    <div className="page-form-banner-bottom-content">
                        <img src={process.env.PUBLIC_URL + '/images/login-rectangle.png'} alt="Rectangle"/>
                    </div>
                </div>

                <div className="page-form">
                    <div className="page-form-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-black.png'} alt="Logo" />
                        <h1 className="page-form-title">Verify Your Identity.</h1>
                        <p className="page-form-subtitle">Please Provide Contact Information.<br />All Social Secuirty Numbers are verified via authenticating.com SentiLink Corp. and Plaid.</p>
                        <div className="page-form-divider" />
                        <FormInputIdVerification />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default IdVerification
