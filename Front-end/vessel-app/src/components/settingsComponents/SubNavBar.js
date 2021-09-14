import React from 'react'
import {
    Nav,
    NavLink,
    Bars,
    NavMenu,
    NavBtn,
    NavBtnLink,
  } from './NavbarElements';
//   src\components\settingsComponents\SettingsNavBarElements
const SubNavBar = () => {
    return (
        <div>
             <Nav>
        <Bars />
  
        <NavMenu>
          <NavLink to='/settings' activeStyle replace>
            Profile
          </NavLink>
          <NavLink to='/account-levels' activeStyle replace>
            Account Verification
          </NavLink>
          <NavLink to='/preferences' activeStyle replace>
            Preferences
          </NavLink>
          <NavLink to='/Financial-services' activeStyle replace>
            Financial Services
          </NavLink>
          <NavLink to='/privacy-rights' activeStyle replace>
            Privacy Rights
          </NavLink>
          <NavLink to='/Linked-accounts' activeStyle replace>
            Linked Accounts
          </NavLink>
          <NavLink to='/crypto-address' activeStyle replace>
            Crypto Address
          </NavLink>
          {/* Second Nav */}
          {/* <NavBtnLink to='/sign-in'>Sign In</NavBtnLink> */}
        </NavMenu>
      </Nav>
        </div>
    )
}

export default SubNavBar
