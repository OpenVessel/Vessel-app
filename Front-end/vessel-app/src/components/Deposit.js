import React, {useContext} from 'react'
import {Context} from "../appContext/UserContext"
import {
    usePlaidLink,
    PlaidLinkOptions,
    PlaidLinkOnSuccess,
    PlaidLinkOnSuccessMetadata,
    PlaidLinkOnExit,
    PlaidLinkOnExitMetadata,
    PlaidLinkError,
  } from 'react-plaid-link';

// The usePlaidLink hook manages Plaid Link creation
// It does not return a destroy function;
// instead, on unmount it automatically destroys the Link instance
const config: PlaidLinkOptions = {
    onSuccess: (public_token, metadata) => {}
    onExit: (err, metadata) => {}
    onEvent: (eventName, metadata) => {}
    token: 'GENERATED_LINK_TOKEN',
    // required for OAuth:
    receivedRedirectUri: window.location.href,
    // if not OAuth, set to null or do not include:
    receivedRedirectUri: null,
  };
  
  const { open, exit, ready } = usePlaidLink(config);

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
    if (userName !== null) {
        // verify phonenumber (ture or False)  -- Where are we saving these?
        // ID or passport     (true or False) 

        // verify existence   (True ) v
        setTimeout(() => {
            actions.VerificationCheck(
            window.sessionStorage.getItem("token_id"), 
            window.sessionStorage.getItem("csrf_token"), 
            window.sessionStorage.getItem("username"));
        }, 5000);
    } 
    
        // when page loads POST /link/token/create initilized plaid link 
        const onSuccess = useCallback<PlaidLinkOnSuccess>(
            (public_token: string, metadata: PlaidLinkOnSuccessMetadata) => {
                // log and save metadata
                // exchange public token
                fetch('//127.0.0.1/exchange-public-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: {
                    public_token,
                },
                });
            },
            [],
        );
    
        // We need to query Plaid API to see if their bank is connect (ping flask app server) 

        
        // Plaid Dialog box
        // connect their bussines account // paypal 
        const { open, exit, ready } = usePlaidLink(config);
        if (ready) { open(); }


        // Dialog rendering inside of here


        const onExit = useCallback<PlaidLinkOnExit>(
            (error: PlaidLinkError, metadata: PlaidLinkOnExitMetadata) => {
                // log and save error and metadata
                // handle invalid link token
                if (error != null && error.error_code === 'INVALID_LINK_TOKEN') {
                // generate new link token
                }
                // to handle other error codes, see https://plaid.com/docs/errors/
            },
            [],
        );


        exit({ force: true });


    return (
        <div>
            <a className="btn-deposit" onClick={handleClick}> Deposit </a>
        </div>
    )
}

export default Deposit
