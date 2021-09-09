
  export default function validateGoogleAPI(values) {
    let errors = {};
    errors.ValidateRequest = true;
     // REGEX ISSUES
  // https://stackoverflow.com/questions/4338267/validate-phone-number-with-javascript
  // implement server side express.js https://github.com/google/libphonenumber
  // https://stackoverflow.com/questions/160550/zip-code-us-postal-code-validation

    if (!values.phonenumber) {
      errors.phonenumber = 'Phone Number required';
      // var isValidZip = /(^\d{5}$)|(^\d{5}-\d{4}$)/.test(values.zipcode);
      errors.ValidateRequest = false;
    } else if (!/^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im.test(values.phonenumber)) {
      errors.phonenumber = 'phonenumber is invalid';
      errors.ValidateRequest = false;
    }

    if (!values.routeName.trim()) {
      errors.routeName = 'route required';
      errors.ValidateRequest = false;
    }
    
    if (!values.state.trim()) {
      errors.state = 'state required';
      // does state exist?
      errors.ValidateRequest = false;
    }

    if (!values.stateName.trim()) {
      errors.stateName = 'stateName required';
      // does state exist?
      errors.ValidateRequest = false;
    }

    if (!values.countryName.trim()) {
      errors.countryName = 'countryName required';
      // does state exist?
      errors.ValidateRequest = false;
    }

    // else if (!/^[A-Za-z]+/.test(values.name.trim())) {
    //   errors.name = 'Enter a valid name';
    // }
    if (!values.residentialaddress.trim()) {
        errors.residentialaddress = 'Residential Address required';
        errors.ValidateRequest = false;
      }

    if (!values.city.trim()) {
        errors.city = 'city required';
        errors.ValidateRequest = false;
    }

    // zipcode validation
    if (!values.zipcode) {
      errors.zipcode = 'zipcode required';
      // var isValidZip = /(^\d{5}$)|(^\d{5}-\d{4}$)/.test(values.zipcode);
      errors.ValidateRequest = false;
    } else if (!/(^\d{5}$)|(^\d{5}-\d{4}$)/.test(values.zipcode)) {
      errors.zipcode = 'zipcode is invalid';
      errors.ValidateRequest = false;
    }

    if (!values.townName) {
      errors.townName = 'townName is required';
      errors.ValidateRequest = false;
    } 
  
    return errors;
  }

// var isValidZip = /(^\d{5}$)|(^\d{5}-\d{4}$)/.test("90210");