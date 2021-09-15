import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import validateID from '../validationCode/validateIdVerification.js';
import useFormIdVerification from '../formCode/useFormIdVerification.js';
import { useHistory  } from 'react-router-dom';
const FormInputIdVerification = ({submitForm}) => {
    
    const {store} = useContext(Context);
    let userName = window.sessionStorage.getItem("username");
    

    const { handleChange, handleSubmit, values, errors } = useFormIdVerification(
        submitForm,
        validateID
    );
    let history = useHistory();
    if(window.sessionStorage.getItem("return_msg") === 'Verification, You are now able to log in') { 
        history.push('/IdVerification')
        sessionStorage.setItem("return_msg", '') 
    }

    return (
        <div>
        <form action="" method="POST" name="register-form" onSubmit={handleSubmit} noValidate>
            {/* we can GET csrf from flask store local session */}
            {/* Hidden Tags */}
            

                <input id="token_id_passback" 
                name="token_id_passback" 
                type="hidden" value={store.token_id}/> 


            
            <input id="csrf_token_passback" 
            name="csrf_token_passback" 
            type="hidden" value={store.csrf_token}/> 

            <input id="username" 
            name="username" 
            type="hidden" 
            value={values.username = userName}/>
            
            {/* Social Secuity Number Inputs */}
            <div className="row inner-row">
            <div className="four columns"> 
                <input type="text"
                name="ssn" 
                placeholder="xxx-xx-xxxx"
                value={values.ssn} 
                onChange={handleChange} />
                {errors.ssn && <p>{errors.ssn}</p>}
            </div>
            </div>

            {/* Date of Birth Input */}
            <div className="row inner-row">
            <div className="four columns"> 
                <input type="date"
                name="DOB" 
                placeholder="Date of Birth" 
                value={values.DOB} 
                onChange={handleChange}  />
                {errors.DOB && <p>{errors.DOB}</p>}
            </div>
            </div>

            {/* CitizenShip  Input*/}
            <div className="row inner-row">
            <div className="four columns"> 
                <input id="citizen" 
                name="CitizenShip"  
                type="text" 
                placeholder="Citizenship" 
                value={values.CitizenShip} 
                onChange={handleChange}   /> 
                {errors.CitizenShip && <p>{errors.CitizenShip}</p>}
            </div>
            </div>

        {/* We need to add in login failed logic */}
            {/* <Link to="/Login"></Link> */}
            <button className="btn-main form-input-btn" 
            type='submit'> 
            Continue </button>

        </form>
                        
        </div>
    )
}

export default FormInputIdVerification
