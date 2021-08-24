import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
//import {Link} from "react-router-dom";
import { Link } from "react-router-dom";
import SideBar from "../components/SideBar.js";
import { useHistory } from "react-router-dom";
import { Search } from "@material-ui/icons"


const apiKey = import.meta.env.VITE_APP_GMAP_API_KEY;
const mapApiJs = 'https://maps.googleapis.com/maps/api/js';


const ContactInfo = () => {
    const history = useHistory();
    const {store, actions} = useContext(Context);
    // const[csrf_token_passback, setCsrftoken] = useState("");
    const[state, setStatename] = useState("");
    const[phonenumber, setPhoneNumber] = useState("");
    const[residentialaddress, setResidentialAddress] = useState("");
    const[city, setCity] = useState("");
    const[zipcode, setZipCode] = useState("");
    const title = 'ContactInfo'
     // using to redirect user to login page 
    const Name = store.firstname
    const username = store.username
    // failling to redirect because both functions are async
    const handleClick = () => { 
        actions.contactinfo( store.token_id, store.csrf_token, phonenumber, residentialaddress, username, city, zipcode);

        // push value we wnat to redirect to "string"
        history.push("/IdVerification");
    };
    
    console.log(store.csrf_token)
    return (
        <div className="container card_registeration">
            <title>{title}</title>


            <div className="registration"> 
                <div className="row outer-row">
                {/* We have component controller component  */}
                {/* <div className="one column">hello</div> */}
                
                {/* Vessel-app\Front-end\vessel-app\src\images */}
                <img src={process.env.PUBLIC_URL + '/images/OV_Logo_Black.png'} alt="OpenVessel2 Logo"/>

                        <h4> <b> Welcome {Name}! </b> </h4>
                        <h6> Please Provide <b> Contact Information </b> </h6>
                        <form action="" method="POST" name="register-form">
                        {/* we can GET csrf from flask store local session */}
                            <input id="token_id_passback" name="token_id_passback" type="hidden" value={store.token_id}/> 
                            <input id="csrf_token_passback" name="csrf_token_passback" type="hidden" value={store.csrf_token}/> 
                            <input type="tel" placeholder="Phone Number" value={phonenumber} onChange={(e) => setPhoneNumber(e.target.value)} />
                        <br></br>
                        <div className="eleven column"> 
                        <input type="text" placeholder="Residential Address" value={residentialaddress} onChange={(e) => setResidentialAddress(e.target.value)} />
                        

                        <div className="search"> 
                        <span> <Search/> </span>
                        <input type="text"/> 
                        </div>

                        </div>
                        <div className="address"> 
                            <div className="row inner-row"> 
                            <div className="six column">
                            <input type="text" placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} />
                            
                            </div>
                            </div>

                            <div className="row inner-row">
                            <div className="two column">
                            <input type="text" placeholder="State" value={state} onChange={(e) => setStatename(e.target.value)} />
                            </div>
                            <div className="two column">    
                            <input id="" placeholder="Zip code" value={zipcode} onChange={(e) => setZipCode(e.target.value)}  /> 
                            </div>
                            </div>
                        </div>
                        </form>
                        <Link to="/IdVerification"> 
                        <button className="btn-main" onClick={handleClick} > Continue </button>
                        </Link>
                {/*   parent row */}
                <div className="four columns"> 
                    <SideBar props={title}> </SideBar>    
                    </div>
            </div>
           
    </div>
</div>
    )
}

export default ContactInfo
