import {useContext, useState, useEffect } from 'react';
import {Context} from "../appContext/UserContext"
const useForm = (callback, validate) => {
  const [values, setValues] = useState({
    username: '',
    firstname:'',
    lastname:'',
    email: '',
    password: '',
    confirmpassword: ''
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
    setIsSubmitting(true);

    if(isSubmitting) {
      console.log(test)
            actions.registration( 
                store.token_id, 
                store.csrf_token, 
                values.firstname, 
                values.lastname, 
                values.username, 
                values.email,
                values.password, 
                values.confirmpassword);
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

export default useForm;