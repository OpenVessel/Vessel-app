import React, {useContext, useState} from 'react'
// import Button from './Button'
import {Link} from "react-router-dom";
import {Context} from "../appContext/UserContext"
import { useHistory } from "react-router";

const Login_Header = (props) => {
    
    const{store, actions } = useContext(Context);
    const history = useHistory();
    // so if user clicks logut it sets token null via actions.logout action
    if (store.token || store.token == "" || store.token == undefined) history.push("/");


    const handleClick = () => { 
        actions.logout();
        
    };
    
    return (
        <header className='header'>
            <div>
            <h1>{props.title} </h1>
            {/* if user is authenticated */}
            <Link to="/Getting_Started"> Getting Started </Link>
            <Link to="/Upload"> Upload </Link>
            <Link to="/Browser"> Browser </Link>
            <Link to="/Account"> Account </Link>
            
            {/* for the user to logout whenever they click this button */}
            {/* <Button onChange={(event => props.onChange(event.target.value))}  onClick={handleClick} text='Log out' value={userCondition} > </Button> */}

            { !store.token ? 
            <Link to="/login"> 
                <button className="btn"> Login Required </button>
            </Link>
            :
                <button onClick={handleClick} className="btn"> Logout </button>
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
