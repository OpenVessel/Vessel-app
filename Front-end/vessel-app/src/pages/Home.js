import React, { useEffect,useContext} from 'react';
import {Context} from "../appContext/UserContext"
import {Link} from "react-router-dom";

function Home() {
    const{store, actions } = useContext(Context);   
    useEffect(()=> {

        if(store.token && store.token !== "" && store.token !== undefined) actions.getMessage();

    }, [store.token]);
    //alt='OpenVessel Logo' style='margin:2%' height='10%' width='50%'
    //https://daveceddia.com/react-image-tag/
    // let imageName = require("/vessel-app/public/OpenVessel_Logo.png")
    // const {value, setValue} = useContext(TestContext);

    return (
        <div>
            <div class="Homepage">

            <img src={process.env.PUBLIC_URL + '/images/OpenVessel_Logo.png'} alt="OpenVessel Logo"/>
            <div class="box"> 
            <Link to="/login" className="btn btn-main">Login</Link>
            <Link to="/register" className=" btn btn-main">Register</Link>
            </div>
            </div>
        </div>
    )
}

export default Home
