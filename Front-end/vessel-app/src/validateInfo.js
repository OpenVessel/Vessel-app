export default function validateInfo(values) {
    let errors = {};
  
    if (!values.username.trim()) {
      errors.username = 'Username required';
    }
    // else if (!/^[A-Za-z]+/.test(values.name.trim())) {
    //   errors.name = 'Enter a valid name';
    // }
    if (!values.firstname.trim()) {
        errors.username = 'First Name required';
      }

    if (!values.lastname.trim()) {
        errors.username = 'Last Name required';
    }

    if (!values.email) {
      errors.email = 'Email required';
    } else if (!/\S+@\S+\.\S+/.test(values.email)) {
      errors.email = 'Email address is invalid';
    }
    if (!values.password) {
      errors.password = 'Password is required';
    } else if (values.password.length < 6) {
      errors.password = 'Password needs to be 6 characters or more';
    }
  
    if (!values.confirmpassword) {
      errors.confirmpassword = 'Password is required';
    } else if (values.confirmpassword !== values.password) {
      errors.confirmpassword = 'Passwords do not match';
    }
    return errors;
  }