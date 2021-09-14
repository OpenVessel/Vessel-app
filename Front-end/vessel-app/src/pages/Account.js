import React from 'react'
import {useLocation } from 'react-router-dom';
import SubRender from '../components/settingsComponents/SubRender';

const Account = () => {
  const location2 = useLocation()
  console.log(location2.pathname)
  // if url changes we conditional render SubNavBar
  if([
  '/account-levels','/Linked-accounts',
  '/privacy-rights','/Financial-services',
    '/preferences','/crypto-address','/settings','/'].includes(location2.pathname)) {
    const localPass = location2.pathname
    return <SubRender localurl={localPass}/> 
    }

    return (
    <div>

  </div>
    )
}

export default Account
