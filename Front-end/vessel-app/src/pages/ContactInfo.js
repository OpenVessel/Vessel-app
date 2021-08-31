import React, {useContext, useState, useEffect} from 'react'
import {Context} from "../appContext/UserContext"
//import {Link} from "react-router-dom";
import { Link } from "react-router-dom";
import SideBar from "../components/SideBar.js";
import { useHistory } from "react-router-dom";
// import { Search } from "@material-ui/icons"
import PlacesAutocomplete, {geocodeByAddress,} from "react-places-autocomplete";



const ContactInfo = () => {

//     const apiKey = import.meta.env.VITE_APP_GMAP_API_KEY;
// const mapApiJs = 'https://maps.googleapis.com/maps/api/js';
    const history = useHistory();
    const {store, actions} = useContext(Context);
    // const[csrf_token_passback, setCsrftoken] = useState("");
    const[state, setStatename] = useState("");
    const[phonenumber, setPhoneNumber] = useState("");
    const[residentialaddress, setResidentialAddress] = useState("");
    const[city, setCity] = useState("");
    const[zipcode, setZipCode] = useState("");
    let title = 'ContactInfo'
     // using to redirect user to login page 
    const Name = store.firstname
    const username = store.username
    // failling to redirect because both functions are async

    function submitForm() {
        setIsSubmitted(true);
    }
    const [isSubmitted, setIsSubmitted] = useState(false)

    const handleSelect = async value => {
        const results = await geocodeByAddress(value);
        console.log(results)
        console.log(results["0"])
        let objAddr = results["0"]
        let objInfo = objAddr["address_components"]
    
        let routeObj = objInfo["0"]
        let townNameObj = objInfo["1"]
        let townShipObj = objInfo["2"]
        let countyNameObj = objInfo["3"]
        let stateNameObj = objInfo["4"]
        let countryNameObj = objInfo["5"]
        let postalCodeObj = objInfo["6"]

        let routeName = routeObj["long_name"]
        let townName = townNameObj["long_name"]
        let townShipName = townShipObj["long_name"]
        let countyName = countyNameObj["long_name"]
        let stateName = stateNameObj["long_name"]
        let countryName = countryNameObj["long_name"]
        let postalName = postalCodeObj["long_name"]


        setResidentialAddress(value);
        setStatename(stateName);
        setCity(townName);
        setZipCode(postalName);
      };
    

    // <script async
//     src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initMap">
// </script>

// // async functtion to load script library from google
// function loadAsyncScript(src) { 
//     return new Promise (executor: resolve => {

//         const script = document.createElement( tagName:"script");
//         Object.assign(script, source{
//             type:"text/javascript",
//             async:true,
//             src
//         })
//         script.addEventListener(type:"load", listener:() => resolve(script));
//         document.head.appendChild(script);
//     })
// }

    // init map script
    // const initMapScript = () => {
    //     // if script already loaded
    //     if(window.google) {
    //         return Promise.resolve();
    //     }
    //     const src = `${mapApiJS}?key=${apiKey}&libraries=places&v=weekly`;
    //     return loadAsyncScript(src)

    // }

    // // load map script after mounted
    // useEffect(() => {
    //     initMapScript().then(() => {
    //     con
    //     })
    // }, []);

    const handleClick = () => { 
        actions.contactinfo( store.token_id, store.csrf_token, phonenumber, residentialaddress, username, city, zipcode);

        // push value we wnat to redirect to "string"
        history.push("/IdVerification");
    };

    console.log(store.csrf_token)
    return (
        <div className="container card_registeration">
            <title>{title}</title>


            <div className="registration"> 
                
                {/* Vessel-app\Front-end\vessel-app\src\images */}
                <img src={process.env.PUBLIC_URL + '/images/OV_Logo_Black.png'} alt="OpenVessel2 Logo"/>
                
                <div className="row outer-row">
                        <h4> <b> Welcome {Name}! </b> </h4>
                        <h6> Please Provide <b> Contact Information </b> </h6>
                        <form action="" method="POST" name="register-form">
                        {/* we can GET csrf from flask store local session */}
                        <input id="token_id_passback" name="token_id_passback" type="hidden" value={store.token_id}/> 
                        <input id="csrf_token_passback" name="csrf_token_passback" type="hidden" value={store.csrf_token}/> 
                        <div className="row inner-row"> 
                            <div className="five column">     
                                <input type="tel" placeholder="Phone Number" value={phonenumber} onChange={(e) => setPhoneNumber(e.target.value)} />
                                <br></br>
                                <PlacesAutocomplete
                                value={residentialaddress}
                                onChange={setResidentialAddress}
                                onSelect={handleSelect}
                            >

                                {/* render props */}
                            {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
                                    <div>
                                        <input {...getInputProps({ placeholder: "Type address" })} />

                                        
                                        <div className="autocomplete-dropdown-container autocss">
                                            {loading && <div><p> Loading... </p></div>}
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


                                </div>
                            </div>
                        {/* </div> */}

                        
                        <div className="row inner-row"> 
                            <div className="address"> 
                                <div className="one column">
                                <input type="text" placeholder="City" value={city} onChange={(e) => setCity(e.target.value)} />
                                
                                </div>
                            </div>
                            <div className="two column">
                            <input type="text" placeholder="State" value={state} onChange={(e) => setStatename(e.target.value)} />
                            </div>
                            <div className="two column">    
                            <input id="text" type="text" pattern="[0-9]{5}" placeholder="Zip code" value={zipcode} onChange={(e) => setZipCode(e.target.value)}  /> 
                            </div>
                        </div>
                        </form>
                        {/* <Link to="/IdVerification">  */}
                        <button className="btn-main" onClick={handleClick} > Continue </button>
                        {/* </Link> */}
                {/*   parent row */}
                <div className="four columns"> 
                    <SideBar title={title}> </SideBar>    
                </div>
            </div>
           
    </div>
</div>
    )
}

export default ContactInfo
