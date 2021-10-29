import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class HomeNavBar extends Component{ 
    state = {clicked:false}

    handleClick = () => {
        this.setState({clicked: !this.state.clicked})
    }
    render() { 
        return( 
        <div>
        <nav className="NavbarItems">
            <Link to="/"> <img src={process.env.PUBLIC_URL + '/images/LogoButtton.PNG'} alt="OpenVessel Logo"/> </Link>
            {/* D:\L_pipe\vessel_app_celery\Vessel-app\Front-end\vessel-app\src\images\LogoButtton.PNG */}
            
            <div className="menu-icon" onClick={this.handleClick}> 
            <i className={this.state.clicked ? 'fas  fa-times' : 'fas fa-bars'}></i>            
            </div>
            <ul className={this.state.clicked ? 'nav-menu active' : 'nav-menu'}> 
            <li className="nav-links" > <Link to="/"> Contact Us </Link> </li>
            <li className="nav-links" > <Link to="/"> Delegates </Link> </li>
            <li className="nav-links" > <Link to="/"> Investors </Link> </li>

            </ul>
        </nav>
        </div>

)
}
    
}

export default HomeNavBar
