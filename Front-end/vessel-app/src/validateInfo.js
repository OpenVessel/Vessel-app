export default function validateInfo(values) {
    let errors = {};
    errors.ValidateRequest = true;
    if (!values.username.trim()) {
      errors.username = 'Username required';
      errors.ValidateRequest = false;
    }
    // else if (!/^[A-Za-z]+/.test(values.name.trim())) {
    //   errors.name = 'Enter a valid name';
    // }
    if (!values.firstname.trim()) {
        errors.username = 'First Name required';
        errors.ValidateRequest = false;
      }

    if (!values.lastname.trim()) {
        errors.username = 'Last Name required';
        errors.ValidateRequest = false;
    }

    if (!values.email) {
      errors.email = 'Email required';
      errors.ValidateRequest = false;
    } else if (!/\S+@\S+\.\S+/.test(values.email)) {
      errors.email = 'Email address is invalid';
      errors.ValidateRequest = false;
    }
    if (!values.password) {
      errors.password = 'Password is required';
      errors.ValidateRequest = false;
    } else if (values.password.length < 6) {
      errors.password = 'Password needs to be 6 characters or more';
      errors.ValidateRequest = false;
    }
  
    if (!values.confirmpassword) {
      errors.confirmpassword = 'Password is required';
      errors.ValidateRequest = false;
    } else if (values.confirmpassword !== values.password) {
      errors.confirmpassword = 'Passwords do not match';
      errors.ValidateRequest = false;
    }
    
    return errors;
  }