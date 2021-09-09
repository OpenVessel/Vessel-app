import React, {useState} from 'react'
import SideBar from "../components/SideBar.js";
import FormSuccess from '../components/FormSuccess';
import FormInputContactInfo from '../components/FormInputContactInfo';

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
        <div className="container card_registeration">
            <title>{title}</title>
            <div className="registration"> 
                <div className="row outer-row">
                <div className="eight columns card_registeration"> 
                {/* Vessel-app\Front-end\vessel-app\src\images */}
                <img src={process.env.PUBLIC_URL + '/images/OVLogoBlack.svg'} alt="OpenVessel Logo" />
                
                        <h4> <b> Welcome {Name}! </b> </h4>
                        <h6> Please Provide <b> Contact Information </b> </h6>
                        {!isSubmitted ? <FormInputContactInfo submitForm={submitForm}/> : <FormSuccess/> }
                        
                {/*   parent row */}
                </div>
                <div className="four columns"> 
                    <SideBar title={title}> </SideBar>    
                </div>
            </div>
           
        </div>
    </div>
</div>
    )
}

export default ContactInfo
