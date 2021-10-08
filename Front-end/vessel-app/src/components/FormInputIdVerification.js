import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import validateID from '../validationCode/validateIdVerification.js';
import useFormIdVerification from '../formCode/useFormIdVerification.js';
import { useHistory  } from 'react-router-dom';
import "../css/page_form.css";
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
                <input id="token_id_passback" name="token_id_passback" type="hidden" value={store.token_id}/>
                <input id="csrf_token_passback" name="csrf_token_passback" type="hidden" value={store.csrf_token}/>
                <input id="username" name="username" type="hidden" value={values.username = userName}/>

                {/* Social Secuity Number Inputs */}
                <div className="page-form-controls">
                    <div className="page-form-control-input-container">
                        <input
                            className="page-form-control-input"
                            id="ssn"
                            type="text"
                            name="ssn"
                            placeholder="xxx-xx-xxxx"
                            value={values.ssn}
                            onChange={handleChange}
                        />
                        <label className="page-form-control-label" htmlFor="ssn">SSN</label>
                        <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <g opacity="0.5">
                                <path d="M17.7083 22.1355H7.29159C3.4895 22.1355 1.302 19.948 1.302 16.1459V8.85423C1.302 5.05215 3.4895 2.86465 7.29159 2.86465H17.7083C21.5103 2.86465 23.6978 5.05215 23.6978 8.85423V16.1459C23.6978 19.948 21.5103 22.1355 17.7083 22.1355ZM7.29159 4.42715C4.31242 4.42715 2.8645 5.87506 2.8645 8.85423V16.1459C2.8645 19.1251 4.31242 20.573 7.29159 20.573H17.7083C20.6874 20.573 22.1353 19.1251 22.1353 16.1459V8.85423C22.1353 5.87506 20.6874 4.42715 17.7083 4.42715H7.29159Z" fill="#414859"/>
                                <path d="M12.4997 13.4063C11.6247 13.4063 10.7393 13.1354 10.0622 12.5834L6.80181 9.9792C6.46848 9.70836 6.40598 9.21878 6.67682 8.88545C6.94765 8.55211 7.43723 8.48962 7.77057 8.76045L11.031 11.3646C11.8226 12 13.1664 12 13.9581 11.3646L17.2185 8.76045C17.5518 8.48962 18.0518 8.5417 18.3122 8.88545C18.5831 9.21878 18.531 9.71878 18.1872 9.9792L14.9268 12.5834C14.2601 13.1354 13.3747 13.4063 12.4997 13.4063Z" fill="#414859"/>
                            </g>
                        </svg>
                    </div>
                    <div className="page-form-control-error">
                        {errors.ssn && <p>{errors.ssn}</p>}
                    </div>
                </div>

                {/* Date of Birth Input */}
                <div className="page-form-controls">
                    <div className="page-form-control-input-container">
                        <input
                            className="page-form-control-input page-form-control-date-input"
                            id="date"
                            type="date"
                            name="DOB"
                            placeholder="Date of Birth:"
                            value={values.DOB}
                            onChange={handleChange}
                        />
                        <label className="page-form-control-label" htmlFor="date">Date of Birth</label>
                    </div>
                    <div className="page-form-control-error">
                        {errors.DOB && <p>{errors.DOB}</p>}
                    </div>
                </div>

                {/* CitizenShip  Input*/}
                <div className="page-form-controls">
                    <div className="page-form-control-input-container">
                        <input
                            className="page-form-control-input"
                            id="citizen"
                            name="CitizenShip"
                            type="text"
                            placeholder="Citizenship"
                            value={values.CitizenShip}
                            onChange={handleChange}
                        />
                        <label className="page-form-control-label" htmlFor="citizen">CitizenShip</label>
                        <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <g opacity="0.5">
                                <path d="M17.7083 22.1355H7.29159C3.4895 22.1355 1.302 19.948 1.302 16.1459V8.85423C1.302 5.05215 3.4895 2.86465 7.29159 2.86465H17.7083C21.5103 2.86465 23.6978 5.05215 23.6978 8.85423V16.1459C23.6978 19.948 21.5103 22.1355 17.7083 22.1355ZM7.29159 4.42715C4.31242 4.42715 2.8645 5.87506 2.8645 8.85423V16.1459C2.8645 19.1251 4.31242 20.573 7.29159 20.573H17.7083C20.6874 20.573 22.1353 19.1251 22.1353 16.1459V8.85423C22.1353 5.87506 20.6874 4.42715 17.7083 4.42715H7.29159Z" fill="#414859"/>
                                <path d="M12.4997 13.4063C11.6247 13.4063 10.7393 13.1354 10.0622 12.5834L6.80181 9.9792C6.46848 9.70836 6.40598 9.21878 6.67682 8.88545C6.94765 8.55211 7.43723 8.48962 7.77057 8.76045L11.031 11.3646C11.8226 12 13.1664 12 13.9581 11.3646L17.2185 8.76045C17.5518 8.48962 18.0518 8.5417 18.3122 8.88545C18.5831 9.21878 18.531 9.71878 18.1872 9.9792L14.9268 12.5834C14.2601 13.1354 13.3747 13.4063 12.4997 13.4063Z" fill="#414859"/>
                            </g>
                        </svg>
                    </div>
                    <div className="page-form-control-error">
                        {errors.CitizenShip && <p>{errors.CitizenShip}</p>}
                    </div>
                </div>

                {/* We need to add in login failed logic */}
                {/* <Link to="/Login"></Link> */}

                <button className="page-form-button" type="submit">Continue</button>
                {<p> {window.sessionStorage.getItem("return_msg")}</p>}
                <div className="page-form-link" />
            </form>
        </div>
    )
}

export default FormInputIdVerification
