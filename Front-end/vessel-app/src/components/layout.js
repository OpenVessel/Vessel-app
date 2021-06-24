// layout components
import React from 'react'
// import Header from './Header'
import Footer from './Footer'

import LoginHeader from './Login_Header'
import LogoutHeader from './Logout_Header'
// let user_condition = { 
//     type:'password',
//     isLoggedIn: false,
// };


const layout = (props) => {
    
    console.log("Layout output", props.title)
    console.log("Layout output", props.isLoggedIn)
    
    if (props.isLoggedIn ===true){ 

        return (
            <div>
                <LoginHeader title={props.title} isLoggedIn={props.isLoggedIn} /> 
    
                <Footer/>
            </div>
        )


    }
    return (
        <div>
            <LogoutHeader title={props.title} isLoggedIn={props.isLoggedIn}  /> 

            <Footer/>
        </div>
    )
}

export default layout
