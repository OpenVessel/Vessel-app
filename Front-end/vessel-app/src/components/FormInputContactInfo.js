import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import PlacesAutocomplete, {geocodeByAddress,} from "react-places-autocomplete";
import validateGoogleAPI from '../validationCode/validateGoogleAPI.js';
import useFormContactInfo from '../formCode/useFormContactInfo.js'
import $ from 'jquery';

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

        console.log(components.route)
        console.log(components.administrative_area_level_1)
        console.log(components.administrative_area_level_2)
        console.log(components.administrative_area_level_3)
        console.log(components.country)
        console.log(components.postal_code)
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
                        <div className="row inner-row"> 
                            <div className="four column">     
                            
                            {/* Phone Number Input */}
                            <input 
                            type="tel"
                            name="phonenumber"
                            placeholder="Phone Number"
                            value={values.phonenumber}
                            onChange={handleChange} 
                            />
                            {errors.phonenumber && <p>{errors.phonenumber}</p>}
                            <br></br>
                            <div> 
                            </div>
                            <div className="row inner-row"> 
                            
                                <div className="four column">
                            <PlacesAutocomplete
                            value={values.residentialaddress=residentialaddress ||residentialaddress}
                            onChange={setResidentialAddress}
                            onSelect={handleSelect}>

                                {/* render props */}
                            {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
                                    <div>
                                        <input {...getInputProps({placeholder: "Type address" })} />

                                        
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
                                        {errors.residentialaddress && <p>{errors.residentialaddress}</p>}
                                    </div>
                                    )}
                            </PlacesAutocomplete>
                            </div>
                                </div>
                            </div>
                            </div>
                        {/* </div> */}

                        
                        <div className="row inner-row"> 
                            <div className="address"> 
                                <div className="four column">
                                {/* City Input  */}
                                <input 
                                type="text" 
                                name="city"
                                placeholder="City" 
                                value={values.city=city || city} 
                                onChange={handleChange} 
                                />
                                {errors.city && <p>{errors.city}</p>}

                                </div>
                            </div>
                            <div className="four column">
                             {/* State Input */}
                                <input 
                                type="text"
                                name="stateName"
                                placeholder="State" 
                                value={values.state=stateName || stateName} 
                                onChange={handleChange} 
                                />
                                {errors.state && <p>{errors.state}</p>}
                            </div>

                            <div className="four column">    
                            {/* Zip Code Input */}
                            <input 
                            id="text" 
                            type="text" 
                            pattern="[0-9]{5}" 
                            placeholder="Zip code" 
                            value={values.zipcode=zipcode || zipcode}
                            onChange={handleChange} 
                            /> 
                            {<p> {window.sessionStorage.getItem("return_msg")}</p>}
                            </div>

                        </div>
                        {/* <Link to="/IdVerification">  */}
                        {/* fix the button */}
                        {errors.zipcode && <p>{errors.zipcode}</p>}
                        <div className="four columns"> 
                            <button className='btn-main form-input-btn' type='submit'>
                            Continue 
                            </button>
                        </div>


                        </form>
        </div>
    )
}

export default FormInputContactInfo