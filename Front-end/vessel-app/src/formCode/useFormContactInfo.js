import {useContext, useState, useEffect } from 'react';
import {Context} from "../appContext/UserContext"

const useFormContactInfo = (callback, validate) => {
  const [values, setValues] = useState({
    state: '',
    phonenumber:'',
    residentialaddress:'',
    username:'',
    city: '',
    zipcode: '',
    routeName: '',
    townName: '',
    townShipName: '',
    countyName: '',
    stateName: '',
    countryName: '',
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
      actions.contactinfo( 
        store.token_id, 
        store.csrf_token, 
        values.phonenumber, 
        values.residentialaddress,
        values.username,
        values.city,
        values.zipcode,
        values.state, 
        values.stateName,
        values.routeName,
        values.townName,
        values.countryName,
        );
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

export default useFormContactInfo;