import React, {useContext, useState, useEffect} from 'react'
// import Button from './Button'
import {Link} from "react-router-dom";
import {Context} from "../appContext/UserContext"
import { useHistory } from "react-router";
import NavBar from "../components/NavBar.js"
const Login_Header = (props) => {
    
    const{store, actions } = useContext(Context);
    console.log("this is your token", store.VerificationStatus)
    const history = useHistory();
    // so if user clicks logut it sets token null via actions.logout action
    if (store.token || store.token === "" || store.token === undefined) history.push("/");
    let title = 'OpenVessel'


        console.log(store.userContactInfo)
        if(store.userContactInfo === false || store.userContactInfo === null){
            console.log(store.username)
            console.log(store.VerificationStatus)
            setTimeout(() => {
                actions.VerificationCheck(
                window.sessionStorage.getItem("token_id"), 
                window.sessionStorage.getItem("csrf_token"), 
                window.sessionStorage.getItem("username"));
            }, 5000);
            
            
        }


    const handleClick = () => { 
        actions.logout();
        
    };
    // logout only works when I referesh the page 
    window.onload = function () {
    document.getElementById("logout").onclick = handleClick;
    }
    return (
        <header>
            <div>

            {/* for the user to logout whenever they click this button */}
            {/* <Button onChange={(event => props.onChange(event.target.value))}  onClick={handleClick} text='Log out' value={userCondition} > </Button> */}
            <NavBar title={title}/>
            { !store.token ? 
            <Link to="/login"> 
                <button className="btn"> Login Required </button>
            </Link>
            :
                <div></div>

            }


            </div>
        </header>
    )
}

// const onClick = (e) => { 
//     // log out functionlity another component? logout button?
//     console.log('click')
// }
// const headingStyle = { 
//     color:'red', backgroundColor: 'black',
// }

export default Login_Header
