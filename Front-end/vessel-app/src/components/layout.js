// layout components
import React, {useContext, useState} from 'react'

import Footer from './Footer'
import LoginHeader from './Login_Header'
import LogoutHeader from './Logout_Header'
import {Context} from "../appContext/UserContext"

const Layout = (props) => {
    const{store, actions } = useContext(Context); //re-render when token is recevied
    console.log("Layout output", props.title)
    

    // Hook useState allows changes in data
    // const [userCondition, setUserCondition] = useState(true);

    // if the user is not logged in it loads the logout header false
    return (
    <div>
        { !store.token ? 
            <div>
            <LogoutHeader title={props.title}  /> 

            <Footer/>
        </div>
            :
            <div>
            
            <LoginHeader title={props.title} /> 

            <Footer/>
        </div>
            }
        
    </div>
    )
}

export default Layout
