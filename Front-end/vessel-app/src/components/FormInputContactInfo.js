import React, {useContext, useState} from 'react';
import {Context} from "../appContext/UserContext";
import PlacesAutocomplete, {geocodeByAddress,} from "react-places-autocomplete";
import validateGoogleAPI from '../validationCode/validateGoogleAPI.js';
import useFormContactInfo from '../formCode/useFormContactInfo.js'
import $ from 'jquery';
import { useHistory  } from 'react-router-dom';
import "../css/page_form.css";
import { Link } from 'react-router-dom';
const FormInputContactInfo = ({submitForm}) => {

    const {store} = useContext(Context);
    const { handleChange, handleSubmit, values, errors } = useFormContactInfo(
        submitForm,
        validateGoogleAPI
    );

    const[residentialaddress, setResidentialAddress] = useState("");
    const[city, setCity] = useState("");
    const[stateName, setStateName] = useState("");
    const[zipcode, setZipCode] = useState("");
    const[routeName, setRouteName] = useState("");
    const[TownShipName, setTownShipName] = useState("");
    const[CountyName, setCountyName] = useState("");
    const[CountryName, setCountryName] = useState("");
    const[userNamePass, setNamePass] = useState("");

    const handleSelect = async value => {

        const results = await geocodeByAddress(value);

        // debug
        // console.log(results["0"])
        // const address =  results.reduce((seed, { long_name, types }) => (types.forEach(t => seed[t] = long_name), seed), {});

        var address_components = results[0].address_components;
        console.log(address_components)
        var components={};
        $.each(address_components, function(k,v1) {$.each(v1.types, function(k2, v2){components[v2]=v1.long_name});});

        // implement dev or debug
        // console.log(components.route)
        // console.log(components.administrative_area_level_1)
        // console.log(components.administrative_area_level_2)
        // console.log(components.administrative_area_level_3)
        // console.log(components.country)
        // console.log(components.postal_code)
        // javascript object has properties from objects, so
        // its a destructuring assignment I guess I will take a wack sunday
        // Essential address compenents for validation
        setResidentialAddress(value)
        setCity(components.locality)
        setStateName(components.administrative_area_level_1)
        setZipCode(components.postal_code)

        // Non essential address components
        setRouteName(components.route)
        setTownShipName(components.administrative_area_level_3)
        setCountyName(components.administrative_area_level_2)
        setCountryName(components.country)
        let userName = window.sessionStorage.getItem("username")
        setNamePass(userName)
      };
      let history = useHistory();
    if(window.sessionStorage.getItem("return_msg") === 'ContactInfo, You are now able to log in') {
        history.push('/IdVerification')
        sessionStorage.setItem("return_msg", '')
    }

    // life cycle reset setItems to defaults
    React.useEffect(() => {
        sessionStorage.setItem("nextpageoffer", 'false') 
    }, []);

    return (
        <div>
             <form action="" method="POST" name="register-form" onSubmit={handleSubmit} noValidate>
                 {/* we can GET csrf from flask store local session */}
                 <input id="token_id_passback" name="token_id_passback" type="hidden" value={store.token_id}/>
                 <input id="csrf_token_passback" name="csrf_token_passback" type="hidden" value={store.csrf_token}/>
                 <input id="username" name="username" type="hidden" value={values.username = userNamePass}/>
                 <input name="routeName" type="hidden" value={values.routeName = routeName || routeName}/>
                 <input name="townName" type="hidden" value={values.townName = city}/>
                 <input name="townShipName" type="hidden" value={values.townShipName = TownShipName}/>
                 <input name="countyName" type="hidden" value={values.countyName = CountyName}/>
                 <input name="stateName" type="hidden" value={values.stateName = stateName}/>
                 <input name="countryName" type="hidden" value={values.countryName = CountryName}/>

                {/* example of Input and CSS */}
                 <div className="page-form-controls">
                      <div className="page-form-control-input-container">
                           <input
                               className="page-form-control-input"
                               type="tel"
                               name="phonenumber"
                               id="phonenumber"
                               value={values.phonenumber}
                               onChange={handleChange}
                               placeholder="Phone Number" />
                           <label className="page-form-control-label" htmlFor="phonenumber">Phone Number</label>
                           <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <g opacity="0.5">
                                    <path d="M17.7083 22.1355H7.29159C3.4895 22.1355 1.302 19.948 1.302 16.1459V8.85423C1.302 5.05215 3.4895 2.86465 7.29159 2.86465H17.7083C21.5103 2.86465 23.6978 5.05215 23.6978 8.85423V16.1459C23.6978 19.948 21.5103 22.1355 17.7083 22.1355ZM7.29159 4.42715C4.31242 4.42715 2.8645 5.87506 2.8645 8.85423V16.1459C2.8645 19.1251 4.31242 20.573 7.29159 20.573H17.7083C20.6874 20.573 22.1353 19.1251 22.1353 16.1459V8.85423C22.1353 5.87506 20.6874 4.42715 17.7083 4.42715H7.29159Z" fill="#414859"/>
                                    <path d="M12.4997 13.4063C11.6247 13.4063 10.7393 13.1354 10.0622 12.5834L6.80181 9.9792C6.46848 9.70836 6.40598 9.21878 6.67682 8.88545C6.94765 8.55211 7.43723 8.48962 7.77057 8.76045L11.031 11.3646C11.8226 12 13.1664 12 13.9581 11.3646L17.2185 8.76045C17.5518 8.48962 18.0518 8.5417 18.3122 8.88545C18.5831 9.21878 18.531 9.71878 18.1872 9.9792L14.9268 12.5834C14.2601 13.1354 13.3747 13.4063 12.4997 13.4063Z" fill="#414859"/>
                                </g>
                           </svg>
                      </div>
                      <div className="page-form-control-error">
                          {errors.phonenumber && <p>{errors.phonenumber}</p>}
                      </div>
                 </div>

                 <div className="page-form-controls">
                     <div>
                          <PlacesAutocomplete
                                value={values.residentialaddress=residentialaddress ||residentialaddress}
                                onChange={setResidentialAddress}
                                onSelect={handleSelect}>

                                {/* render props */}
                                {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
                                    <div className="page-form-control-input-container">
                                        <input {...getInputProps({placeholder: "Type address", id: "address", className: "page-form-control-input" })} />
                                        <label className="page-form-control-label" htmlFor="address">Address</label>
                                        <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <g opacity="0.5">
                                                 <path d="M17.7083 22.1355H7.29159C3.4895 22.1355 1.302 19.948 1.302 16.1459V8.85423C1.302 5.05215 3.4895 2.86465 7.29159 2.86465H17.7083C21.5103 2.86465 23.6978 5.05215 23.6978 8.85423V16.1459C23.6978 19.948 21.5103 22.1355 17.7083 22.1355ZM7.29159 4.42715C4.31242 4.42715 2.8645 5.87506 2.8645 8.85423V16.1459C2.8645 19.1251 4.31242 20.573 7.29159 20.573H17.7083C20.6874 20.573 22.1353 19.1251 22.1353 16.1459V8.85423C22.1353 5.87506 20.6874 4.42715 17.7083 4.42715H7.29159Z" fill="#414859"/>
                                                 <path d="M12.4997 13.4063C11.6247 13.4063 10.7393 13.1354 10.0622 12.5834L6.80181 9.9792C6.46848 9.70836 6.40598 9.21878 6.67682 8.88545C6.94765 8.55211 7.43723 8.48962 7.77057 8.76045L11.031 11.3646C11.8226 12 13.1664 12 13.9581 11.3646L17.2185 8.76045C17.5518 8.48962 18.0518 8.5417 18.3122 8.88545C18.5831 9.21878 18.531 9.71878 18.1872 9.9792L14.9268 12.5834C14.2601 13.1354 13.3747 13.4063 12.4997 13.4063Z" fill="#414859"/>
                                            </g>
                                        </svg>

                                        <div className="autocomplete-dropdown-container autocss">
                                            {loading && <div></div>}
                                            {suggestions.map(suggestion => {
                                                    const className = suggestion.active
                                                        ? 'suggestion-item--active'
                                                        : 'suggestion-item';
                                                    // inline style for demonstration purpose
                                                    const style = suggestion.active
                                                        ? { backgroundColor: '#fafafa', cursor: 'pointer' }
                                                        : { backgroundColor: '#ffffff', cursor: 'pointer' };
                                                    return (
                                                        <div
                                                            {...getSuggestionItemProps(suggestion, {
                                                                className,
                                                                style,
                                                            })}
                                                        >
                                                            <span>{suggestion.description}</span>
                                                        </div>
                                                    );
                                            })}
                                        </div>
                                    </div>
                                )}
                          </PlacesAutocomplete>
                          <div className="page-form-control-error">
                             {errors.residentialaddress && <p>{errors.residentialaddress}</p>}
                          </div>
                     </div>
                 </div>

                 <div className="page-form-controls">
                      <div className="page-form-control-input-container">
                          <input
                              className="page-form-control-input"
                              id="city"
                              type="text"
                              name="city"
                              placeholder="City"
                              value={values.city=city || city}
                              onChange={handleChange}/>
                          <label className="page-form-control-label" htmlFor="city">City</label>
                          <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                               <g opacity="0.5">
                                   <path d="M17.7083 22.1355H7.29159C3.4895 22.1355 1.302 19.948 1.302 16.1459V8.85423C1.302 5.05215 3.4895 2.86465 7.29159 2.86465H17.7083C21.5103 2.86465 23.6978 5.05215 23.6978 8.85423V16.1459C23.6978 19.948 21.5103 22.1355 17.7083 22.1355ZM7.29159 4.42715C4.31242 4.42715 2.8645 5.87506 2.8645 8.85423V16.1459C2.8645 19.1251 4.31242 20.573 7.29159 20.573H17.7083C20.6874 20.573 22.1353 19.1251 22.1353 16.1459V8.85423C22.1353 5.87506 20.6874 4.42715 17.7083 4.42715H7.29159Z" fill="#414859"/>
                                   <path d="M12.4997 13.4063C11.6247 13.4063 10.7393 13.1354 10.0622 12.5834L6.80181 9.9792C6.46848 9.70836 6.40598 9.21878 6.67682 8.88545C6.94765 8.55211 7.43723 8.48962 7.77057 8.76045L11.031 11.3646C11.8226 12 13.1664 12 13.9581 11.3646L17.2185 8.76045C17.5518 8.48962 18.0518 8.5417 18.3122 8.88545C18.5831 9.21878 18.531 9.71878 18.1872 9.9792L14.9268 12.5834C14.2601 13.1354 13.3747 13.4063 12.4997 13.4063Z" fill="#414859"/>
                               </g>
                          </svg>
                      </div>
                      <div className="page-form-control-error">
                          {errors.city && <p>{errors.city}</p>}
                      </div>
                 </div>

                 <div className="page-form-controls">
                      <div className="page-form-control-input-container">
                          <input
                              className="page-form-control-input"
                              id="state"
                              type="text"
                              name="stateName"
                               placeholder="State"
                               value={values.state=stateName || stateName}
                               onChange={handleChange}/>
                          <label className="page-form-control-label" htmlFor="state">State</label>
                          <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                               <g opacity="0.5">
                                   <path d="M17.7083 22.1355H7.29159C3.4895 22.1355 1.302 19.948 1.302 16.1459V8.85423C1.302 5.05215 3.4895 2.86465 7.29159 2.86465H17.7083C21.5103 2.86465 23.6978 5.05215 23.6978 8.85423V16.1459C23.6978 19.948 21.5103 22.1355 17.7083 22.1355ZM7.29159 4.42715C4.31242 4.42715 2.8645 5.87506 2.8645 8.85423V16.1459C2.8645 19.1251 4.31242 20.573 7.29159 20.573H17.7083C20.6874 20.573 22.1353 19.1251 22.1353 16.1459V8.85423C22.1353 5.87506 20.6874 4.42715 17.7083 4.42715H7.29159Z" fill="#414859"/>
                                   <path d="M12.4997 13.4063C11.6247 13.4063 10.7393 13.1354 10.0622 12.5834L6.80181 9.9792C6.46848 9.70836 6.40598 9.21878 6.67682 8.88545C6.94765 8.55211 7.43723 8.48962 7.77057 8.76045L11.031 11.3646C11.8226 12 13.1664 12 13.9581 11.3646L17.2185 8.76045C17.5518 8.48962 18.0518 8.5417 18.3122 8.88545C18.5831 9.21878 18.531 9.71878 18.1872 9.9792L14.9268 12.5834C14.2601 13.1354 13.3747 13.4063 12.4997 13.4063Z" fill="#414859"/>
                               </g>
                           </svg>
                      </div>
                      <div className="page-form-control-error">
                          {errors.state && <p>{errors.state}</p>}
                      </div>
                 </div>

                 <div className="page-form-controls">
                      <div className="page-form-control-input-container">
                          <input
                              className="page-form-control-input"
                              name="zipcodeName"
                              id="text"
                              type="text"
                              pattern="[0-9]{5}"
                              placeholder="Zip Code"
                              value={values.zipcode=zipcode || zipcode}
                              onChange={handleChange}/>
                          <label className="page-form-control-label" htmlFor="text">Zip Code</label>
                          <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <g opacity="0.5">
                                  <path d="M17.7083 22.1355H7.29159C3.4895 22.1355 1.302 19.948 1.302 16.1459V8.85423C1.302 5.05215 3.4895 2.86465 7.29159 2.86465H17.7083C21.5103 2.86465 23.6978 5.05215 23.6978 8.85423V16.1459C23.6978 19.948 21.5103 22.1355 17.7083 22.1355ZM7.29159 4.42715C4.31242 4.42715 2.8645 5.87506 2.8645 8.85423V16.1459C2.8645 19.1251 4.31242 20.573 7.29159 20.573H17.7083C20.6874 20.573 22.1353 19.1251 22.1353 16.1459V8.85423C22.1353 5.87506 20.6874 4.42715 17.7083 4.42715H7.29159Z" fill="#414859"/>
                                  <path d="M12.4997 13.4063C11.6247 13.4063 10.7393 13.1354 10.0622 12.5834L6.80181 9.9792C6.46848 9.70836 6.40598 9.21878 6.67682 8.88545C6.94765 8.55211 7.43723 8.48962 7.77057 8.76045L11.031 11.3646C11.8226 12 13.1664 12 13.9581 11.3646L17.2185 8.76045C17.5518 8.48962 18.0518 8.5417 18.3122 8.88545C18.5831 9.21878 18.531 9.71878 18.1872 9.9792L14.9268 12.5834C14.2601 13.1354 13.3747 13.4063 12.4997 13.4063Z" fill="#414859"/>
                              </g>
                          </svg>
                      </div>
                      <div className="page-form-control-error">
                          {errors.zipcode && <p>{errors.zipcode}</p>}
                      </div>
                 </div>

                 {/* <Link to="/IdVerification">  */}
                 {/* fix the button */}

                 <button className="page-form-button" type="submit">Continue</button>
                
                 {window.sessionStorage.getItem("nextpageoffer") === 'true' &&
                    <div>
                        <div className='respCss'> 
                        <p> {window.sessionStorage.getItem("return_msg")} </p>
                        </div>
                        <div cassName='smalltext'> <p>Check out  <Link to="/contactInfo"> Contact  Info </Link> </p>  
                        </div> 
                    </div> 
                    }

                 <div className="page-form-link" />
             </form>
        </div>
    )
}

export default FormInputContactInfo
