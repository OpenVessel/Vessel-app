import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
//import {Link} from "react-router-dom";
import { Link } from "react-router-dom";
import SideBar from "../components/SideBar.js";
import { useHistory } from "react-router-dom";

const IdVerification = () => {
    const history = useHistory();
    const {store, actions} = useContext(Context);
    const[DOB, setDob] = useState("");
    const[ssn, setSsnname] = useState("");
    const[citizenship, setCitizenship] = useState("");
    let title = 'Verification'
    const username = store.username
     // using to redirect user to login page 

    // failling to redirect because both functions are async
    const handleClick = () => { 
        actions.Verification(  store.token_id, store.csrf_token, username, ssn, DOB, citizenship);
        // actions.redirect(store.return_msg);
        // history.push("/login");
        // push value we wnat to redirect to "string"
        // history.push("/Login");
    };
    
    console.log(store.csrf_token)
    return (
        <div className="container card_registeration">
            <title>{title}</title>


            <div className="registration"> 
                <div className="row outer-row ">
                {/* We have component controller component  */}
                {/* <div className="one column">hello</div> */}
                
                    
                    <img src={process.env.PUBLIC_URL + '/images/OV_Logo_Black.png'} alt="OpenVessel2 Logo"/>
                        <h4> <b> Verify Your Identity</b> </h4>
                        <h6> Please Provide <b> Contact Information </b> </h6>
                        <form action="" method="POST" name="register-form">
                        {/* we can GET csrf from flask store local session */}
                        <input id="token_id_passback" name="token_id_passback" type="hidden" value={store.token_id}/> 
                        <input id="csrf_token_passback" name="csrf_token_passback" type="hidden" value={store.csrf_token}/> 
                        <input type="text" placeholder="Social Security number " value={ssn} onChange={(e) => setSsnname(e.target.value)} />
                        <input type="text" placeholder="Date of Birth" value={DOB} onChange={(e) => setDob(e.target.value)} />
                        <input id="citizen" type="text" placeholder="Citizenship" value={citizenship} onChange={(e) => setCitizenship(e.target.value)}  /> 

                        </form>

                        {/* We need to add in login failed logic */}
                        <Link to="/Login">
                        <button className="btn-main" onClick={handleClick} > Continue </button>
                        </Link>

                    <div className="four columns"> 
                    <SideBar title={title}> </SideBar>    
                    </div>
                {/*   parent row */}
            </div>
    </div>
</div>
    )
}

export default IdVerification
