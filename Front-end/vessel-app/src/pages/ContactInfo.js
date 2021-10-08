import React, {useState} from 'react';
import FormSuccess from '../components/FormSuccess';
import FormInputContactInfo from '../components/FormInputContactInfo';
import "../css/page_form.css";

const ContactInfo = () => {
    const Name = window.sessionStorage.getItem("firstname")
    let title = 'ContactInfo'
    function submitForm() {
        setIsSubmitted(true);
    }
    const [isSubmitted, setIsSubmitted] = useState(false);

    // whenever our page refreshes it set the context value to its default.
    return (
        <div>
            <div className="container page-form-container register-container">
                <div className="page-form">
                    <div className="page-form-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-black.png'} alt="Logo" />
                        <h1 className="page-form-title">Welcome {Name}!</h1>
                        <p className="page-form-subtitle">Please provide Contact Information.</p>
                        <div className="page-form-divider" />
                        {!isSubmitted ? <FormInputContactInfo submitForm={submitForm}/> : <FormSuccess/> }
                    </div>
                </div>

                <div className="page-form-banner" style={{backgroundImage: "url(" + process.env.PUBLIC_URL + '/images/login-banner.png' + ")"}}>
                    <div className="page-form-banner-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-white.png'} alt="Logo"/>
                        <h1>Out-of-Pocket<br /> Insurance Premium.</h1>
                        <p>Make monthly payments of low-end $150 to pay off medical bills with small to large ducbuitles debt. To high-end premium of $300.</p>
                    </div>
                    <div className="page-form-banner-bottom-content">
                        <img src={process.env.PUBLIC_URL + '/images/login-rectangle.png'} alt="Rectangle"/>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ContactInfo
