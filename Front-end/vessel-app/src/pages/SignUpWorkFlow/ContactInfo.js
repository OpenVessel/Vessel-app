import React, {useState} from 'react';
import FormSuccess from '../../components/FormSuccess';
import FormInputContactInfo from '../../components/FormInputContactInfo';
import "../../css/page_form.css";
import ContactInfoContent from './content/ContactInfoContent';

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
                        <p className="page-form-bold">Please provide Contact Information.</p>
                        <div className="page-form-divider" />
                        {!isSubmitted ? <FormInputContactInfo submitForm={submitForm}/> : <FormSuccess/> }
                    </div>
                </div>
                {/* height: 1024 px width: 708 px */}
                <div className="page-form-banner" style={{backgroundImage: "url(" + process.env.PUBLIC_URL + '/images/ContactInfoPageImage.jpg' + ")", 
                }}>
                    <div className="page-form-banner-content">
                        <img src={process.env.PUBLIC_URL + '/images/logo-white.png'} alt="Logo"/>
                        <ContactInfoContent></ContactInfoContent>
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
