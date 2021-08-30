import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import useForm from './useForm'
import validate from '../validateInfo';
    
const FormInput = ({submitForm}) => {
    const {store, actions} = useContext(Context);

    const { handleChange, handleSubmit, values, errors } = useForm(
        submitForm,
        validate
      );

    return (
        <div>
             <form action="" method="POST" name="register-form" onSubmit={handleSubmit}>
                        {/* we can GET csrf from flask store local session */}
                        <input id="token_id_passback" name="token_id_passback" type="hidden" value={store.token_id}/> 
                        <input id="csrf_token_passback" name="csrf_token_passback" type="hidden" value={store.csrf_token}/> 
                        <div className="row inner-row ">
                            <div className="four columns"> 
                                
                                {/* First Name Section */}
                                <input
                                type="text" 
                                name="firstname"
                                placeholder="First Name" 
                                className="form-input"
                                value={values.firstname} 
                                onChange={handleChange} 
                                />
                                {errors.firstname && <p>{errors.firstname}</p>}
                            </div>
                            <div className="four columns"> 
                                {/* Last Name */}
                                <input 
                                type="text" 
                                name="lastname"
                                className="form-input"
                                placeholder="Last Name" 
                                value={values.lastname} 
                                onChange={handleChange} />
                                {errors.lastname && <p>{errors.lastname}</p>}
                            </div>
                        </div>

                        <div className="row inner-row">
                            <div className="four columns"> 
                                {/* username input */}
                                <input 
                                type="text" 
                                name="username"
                                placeholder="username"
                                className="form-input" 
                                value={values.username} 
                                onChange={handleChange} 
                                />
                                {errors.username && <p>{errors.username}</p>}
                            </div>
                            <div className="four columns"> 
                                {/* Email Input */}
                                <input 
                                type="text" 
                                name="email"
                                placeholder="email" 
                                className="form-input"
                                value={values.email} 
                                onChange={handleChange}
                                />
                                {errors.email && <p>{errors.email}</p>}
                            </div>
                        </div>

                        <div className="row inner-row">
                            <div className="four columns"> 
                            {/* password input */}
                                <input id="password"
                                placeholder="password" 
                                required type="password" 
                                name="password"
                                className="form-input"
                                value={values.password} 
                                onChange={handleChange} 
                                /> 
                                {errors.password && <p>{errors.password}</p>}
                            </div>

                            <div className="four columns"> 
                            
                            {/* Confirm Input */}
                            <input 
                            id="confirm_password" 
                            name="confirmpassword" 
                            required type="password" 
                            className="form-input"
                            placeholder="Confirm Password" 
                            value={values.confirmpassword} 
                            onChange={handleChange}/>

                            {errors.confirmpassword && <p>{errors.confirmpassword}</p>}

                            </div>
                        </div>
                        </form>
        </div>
    )
}

export default FormInput
