import React, { Component } from 'react';
import {Link} from "react-router-dom";


class NavBar extends Component{ 
    state = {clicked:false}

    handleClick = () => {
        this.setState({clicked: !this.state.clicked})
    }
    // const handleLogOut = () => { 
    //     actions.logout();
        
    // };

    render() { 
    return( 
        <nav className="NavbarItems">
        <Link to="/"> <h1 className="navbar-logo">{this.props.title} </h1> </Link>

        <div className="menu-icon" onClick={this.handleClick}> 
        <i className={this.state.clicked ? 'fas  fa-times' : 'fas fa-bars'}></i>            
        </div>
        <ul className={this.state.clicked ? 'nav-menu active' : 'nav-menu'}> 
        <li className="nav-links" > <Link to="/EMF">  Emergency Medical Fund  </Link> </li>
        <li className="nav-links"> <Link to="/Upload"> Upload </Link> </li>
        <li className="nav-links"> <Link to="/Browser"> Coverage </Link> </li>
        <li className="nav-links"> <Link to="/Account"> Account </Link> </li>
        <li className="nav-links"> <Link to="/Buy"> Buy </Link> </li>
        <button id="logout" className="btn"> Logout </button> 
        </ul>
        </nav>

    )
    }
        
}

export default NavBar