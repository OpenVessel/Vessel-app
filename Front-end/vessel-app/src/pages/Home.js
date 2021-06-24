import React, {useContext} from 'react';
import { TestContext } from '../appContext/testContext';
import {Link} from "react-router-dom";

function Home() {

    //alt='OpenVessel Logo' style='margin:2%' height='10%' width='50%'
    //https://daveceddia.com/react-image-tag/
    // let imageName = require("/vessel-app/public/OpenVessel_Logo.png")
    const {value, setValue} = useContext(TestContext);

    return (
        <div>
            <div> Home page</div>

            <img src={process.env.PUBLIC_URL + '/images/OpenVessel_Logo.png'} alt="OpenVessel Logo"/>
            <div> {value}</div>
            <Link to="/login" className="btn btn-primary">Login</Link>
            <Link to="/register" className="btn btn-primary">Register</Link>

        </div>
    )
}

export default Home
