import {useContext, useState, useEffect } from 'react';
import {Context} from "../appContext/UserContext"

const useForm = (callback, validate) => {
  const [values, setValues] = useState({
    username: '',
    firstname:'',
    lastname:'',
    email: '',
    password: '',
    confirmpassword: '',
    ValidateRequest:false
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [msg, setReturnMsg] = useState("");
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
    setIsSubmitting(true);


    if(isSubmitting && errors.ValidateRequest === true) {
      console.log(isSubmitting, "test")
            actions.registration( 
                store.token_id, 
                store.csrf_token, 
                values.firstname, 
                values.lastname, 
                values.username, 
                values.email,
                values.password, 
                values.confirmpassword);
                
                console.log(window.sessionStorage.getItem("return_msg"))
              // submit on request Success this triggers redirect?
    // setReturnMsg(window.sessionStorage.getItem("return_msg"))
    // if(msg === 'Your account has been created! You are now able to log in'){ 
    //   console.log
    // 
    // }
    const moveOn = false
    console.log(errors.ValidateRequest)
    if(errors.ValidateRequest === true) {
            console.log("hello movOn Trigger")
            if(window.sessionStorage.getItem("return_msg") === 'Your account has been created! You are now able to log in') { 
                const moveOn = true
            }
          }  
  
            
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

  return { handleChange, handleSubmit, values, errors};
};

export default useForm;