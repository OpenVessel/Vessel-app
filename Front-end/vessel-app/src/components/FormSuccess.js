import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"

const FormSuccess = () => {
    const {store, actions} = useContext(Context);
    return (
    <div className='form-content-right'>
                      <h1> {store.return_msg}</h1>
    </div>
  );
};

export default FormSuccess;