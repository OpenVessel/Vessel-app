// layout components
import React, { useState } from 'react';

import Footer from './Footer'
import LoginHeader from './Login_Header'
import LogoutHeader from './Logout_Header'

const Layout = (props) => {
    
    console.log("Layout output", props.title)
    console.log("Layout output", props.isLoggedIn)
    

    // Hook useState allows changes in data
    const [userCondition, setUserCondition] = useState(true);

    // Implement debug logic here
    console.log("Layout - userCondition", userCondition)
    if (userCondition === true){ 

        // if the user is logged in it loads the Login headers true
        return (
            <div>
                <p> is the user login? {userCondition} </p>
                <LoginHeader title={props.title} isLoggedIn={props.isLoggedIn} onChange={(value => setUserCondition(value))}/> 
    
                <Footer/>
            </div>
        )


    }
    // if the user is not logged in it loads the logout header false
    return (
        <div>
            <LogoutHeader title={props.title} isLoggedIn={props.isLoggedIn}  /> 

            <Footer/>
        </div>
    )
}

export default Layout
