import React, {useContext, useState} from 'react'
import Button from './Button'
import {Link} from "react-router-dom";
import {Context} from "../appContext/UserContext"

const Login_Header = (props) => {
    
    const{store, actions } = useContext(Context);
    console.log( "Login Header - props -> ", props)
    console.log("is boolean pasing", props.isLoggedIn)
    console.log(props.onChange)
    let userCondition = props.onChange.userCondition

    // handleClick will change the onChange
    const handleClick = () => {

        console.log("changing userCondition", userCondition)
        userCondition = false;
        //onChange={(event => props.onChange(event.target.value ))} 
        //onChange= userCondition
        console.log("changing userCondition", userCondition)
    }

    return (
        <header className='header'>
            <h1 style ={headingStyle}>{props.title} </h1>
            {/* if user is authenticated */}
            <Link to="/"> Home </Link>
            <Link to="/Getting_Started"> Getting Started </Link>
            <Link to="/Upload"> Upload </Link>
            <Link to="/Browser"> Browser </Link>
            <Link to="/Account"> Account </Link>

            
            
            {/* for the user to logout whenever they click this button */}
            <Button onChange={(event => props.onChange(event.target.value))}  onClick={handleClick} text='Log out' value={userCondition} > </Button>
        </header>
    )
}

// const onClick = (e) => { 
//     // log out functionlity another component? logout button?
//     console.log('click')
// }



const headingStyle = { 
    color:'red', backgroundColor: 'black',
}

export default Login_Header
