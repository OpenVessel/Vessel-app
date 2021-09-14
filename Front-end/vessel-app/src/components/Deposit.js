import React, {useContext} from 'react'
import {Context} from "../appContext/UserContext"

const Deposit = () => {
    const{store, actions } = useContext(Context);
    const userName = window.sessionStorage.getItem("username")
    function handleClick(e) {    
        e.preventDefault();   
        console.log('The link was clicked.');  
    
    // generate and save a Link token is sessionstore
    // flask API call to
    actions.PlaidEntryPoint(store.token, store.csrf_token, userName);
    }
    // user's Action around the direct click
    // So when the user clicks depoist we need to do a seriers of checks 

    // We need code that checks the flask app to see if the user is Verified table
        // verify phonenumber (ture or False)
        // ID or passport     (true or False)
        // verify existence   (True )  
        
        // when page loads POST /link/token/create initilized plaid link 
    
        // We need to query Plaid API to see if their bank is connect (ping flask app server) 
        
        // Plaid Dialog box
        // connect their bussines account // paypal 
    
        // Dialog rendering inside of here

    return (
        <div>
            <a className="btn-deposit" onClick={handleClick}> Deposit </a>
        </div>
    )
}

export default Deposit
