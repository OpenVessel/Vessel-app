import {useContext, useState, useEffect } from 'react';
import {Context} from "../appContext/UserContext"

const useFormIdVerification = (callback, validate) => {
  const [values, setValues] = useState({
    snn: '',
    DOB: '',
    CitizenShip: '',
    username:'',
    ValidateRequest:false
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const {store, actions} = useContext(Context);

  const handleChange = e => {
    const { name, value } = e.target;
    setValues({
      ...values,
      [name]: value
    });
  };

  const handleSubmit = e => {
    e.preventDefault();

    setErrors(validate(values));
    //we have to implement does user exist already logic or email? 
    // server side validation
    setIsSubmitting(true);
    console.log(errors.ValidateRequest)
    if(isSubmitting && errors.ValidateRequest === true) {
      console.log(isSubmitting, "test")
      actions.Verification(  
        store.token_id, 
        store.csrf_token, 
        values.username, 
        values.ssn, 
        values.DOB, 
        values.CitizenShip);
    }

  };

  useEffect(
    () => {
      if (Object.keys(errors).length === 0 && isSubmitting) {
        callback();
      }
    },
    [errors]
  );

  return { handleChange, handleSubmit, values, errors };
};

export default useFormIdVerification;