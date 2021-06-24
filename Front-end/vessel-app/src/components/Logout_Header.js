import React from 'react'
import {Link} from "react-router-dom";

const Logout_Header = (props) => {
    console.log("User Logged Out")
    return (
        <header className='header'>
            <h1 style ={headingStyle}>{props.title} </h1>
            
            {/* else  */}
            <Link to="/"> Home </Link>
            <Link to="/Getting_Started"> Getting Started </Link>
            <Link to="/Login"> Login </Link>
            
            {/* <Button onClick={onClick} text='Home'> </Button>
            <Button text='Getting Started'> </Button>

            <Button text='Login'> </Button> */}
        </header>
    )
}


const headingStyle = { 
    color:'red', backgroundColor: 'black',
}

export default Logout_Header
