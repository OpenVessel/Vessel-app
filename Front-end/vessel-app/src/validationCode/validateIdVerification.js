
  export default function validateIdVerification(values) {
    
    let errors = {};
    errors.ValidateRequest = true;
    // REGEX ISSUES
  var patt = new RegExp("\d{3}[\-]\d{2}[\-]\d{4}");
  
  // validate SSN http://zparacha.com/validate-social-security-number-using-javascript-regular-expressions
    if (!values.ssn) {
      errors.ssn = 'Social Security Number required';
      // var isValidZip = /(^\d{5}$)|(^\d{5}-\d{4}$)/.test(values.zipcode);
      errors.ValidateRequest = false;
    } else if (patt.test(values.ssn)) {
      errors.ssn = 'Social Security is invalid';
      errors.ValidateRequest = false;
    }

    if (!values.CitizenShip) {
      console.log("debug", values.CitizenShip)
      errors.CitizenShip = 'Citizenship required';
      errors.ValidateRequest = false;
    }
    
    if (!values.DOB) {
      errors.DOB = 'Date Of Birth required';
      // does state exist?
      errors.ValidateRequest = false;
    }

    return errors;
  }
