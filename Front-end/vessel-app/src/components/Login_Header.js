import React from 'react'
import Button from './Button'
import {Link} from "react-router-dom";

const Login_Header = (props) => {
    
    console.log(props.title)
    
    return (
        <header className='header'>
            <h1 style ={headingStyle}>{props.title} </h1>
            {/* if user is authenticated */}
            <Link to="/"> Home </Link>
            <Link to="/Getting_Started"> Getting Started </Link>
            <Link to="/Upload"> Upload </Link>
            <Link to="/Browser"> Browser </Link>
            <Link to="/Account"> Account </Link>
            
            <Button text='Log out'> </Button>
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
