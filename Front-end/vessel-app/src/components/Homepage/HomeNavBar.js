import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import "../../css/HomePage.css"
class HomeNavBar extends Component{ 
    state = {clicked:false}

    handleClick = () => {
        this.setState({clicked: !this.state.clicked})
    }
    render() { 
        return( 
        <div className="HeaderCss">
             <img src={process.env.PUBLIC_URL + '/images/OV_Logo_Black.png'} alt="OpenVessel Logo"/>
            <nav>
                <ul className="nav__links">    
                    <li><Link to="/about">  About Us </Link> </li>
                    <li><Link to="/compliance">  Compliance </Link> </li>
                    <li><Link to="/delegates"> Delegates </Link> </li>
                    <li><Link to="/investors"> Investors </Link> </li>
                </ul>
            </nav>
            <button> <Link to="ContactUs"> Contact Us</Link> </button>
        </div>

)
}
    
}

export default HomeNavBar
