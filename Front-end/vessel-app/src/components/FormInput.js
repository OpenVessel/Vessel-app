import React, {useContext} from 'react'
import {Context} from "../appContext/UserContext"
import useForm from '../formCode/useForm'
import validate from '../validateInfo';
import { Link, useHistory  } from 'react-router-dom';
import SignUpBtn from '../components/SignUpButtton'
const FormInput = ({submitForm}) => {
    const {store} = useContext(Context);
    
    const { handleChange, handleSubmit, values, errors, moveOn } = useForm(
        submitForm,
        validate
      );
    
    let history = useHistory();
    if(window.sessionStorage.getItem("return_msg") === 'Your account has been created! You are now able to log in') { 
        history.push('/contactInfo')
        sessionStorage.setItem("return_msg", '') 
    }

    return (
        <div>
             <form action="" method="POST" name="register-form"  autoComplete="off" onSubmit={handleSubmit} noValidate>
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
                                autoComplete="new-password"
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
                                autocomplete="new-password"
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
                            <div className="four columns"> 
                            
                            
                            <button  className='btn-main form-input-btn' type='submit'>
                            Sign Up
                            </button>
                            {<p> {window.sessionStorage.getItem("return_msg")}</p>}
                            {/* <SignUpBtn moveOn={errors.ValidateRequest} /> */}

                            

                            <span className='form-input-login'>
                            Already have an account? Login <Link to="/Login">  here</Link>
                            </span>


                            </div>
                           
                        </div>
                        </form>
        </div>
    )
}

export default FormInput
