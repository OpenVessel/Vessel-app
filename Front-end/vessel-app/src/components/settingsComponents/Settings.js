import React, {useContext, useState} from 'react'
import {Context} from "../../appContext/UserContext"
import profileImg from '../../images/default_user.png'

const Settings = () => {

    const{store, actions } = useContext(Context);
    const[email, setEmail] = useState("");
    const Webpage = 'Account'
    const username = store.username
    const DisplayEmail = store.email

  const [image, setImage] = useState({ preview: profileImg, raw: "" });

  // const handleChange = e => {
  //   console.log(e.target.files[0]);
  //   if (e.target.files.length) {
  //     setImage({
  //       preview: URL.createObjectURL(e.target.files[0]),
  //       raw: e.target.files[0]
  //     });
  //   }
  // };


    const handleClick = () => { 
      console.log("Hello World")
      

      actions.changeAccount( store.token_id, 
          store.csrf_token, 
          username, 
          email,
          Webpage,
          image
          );
    // we need a function from actions to send post request to flask to update account information
      // history.push("/login");
  };


    return (
        <div>
            {/* <!-- ACCOUNT HEADER --> */}
        <div className="account-section">
        <div className="minibox"> 
        <label className="custom-field-settings"> 
        <h2> My Profile </h2> 
          <form> 
          <p> Display name </p> 
          <input 
            type="text"
            id="changeName"
            onChange={handleClick}
            />

            <p> Email address</p>
            <input
            type="text"
            id="changeName"
            onChange={handleClick}
            />

          <input
              type="file"
              id="upload-button"
              style={{ display: "none" }}
              onChange={handleClick}
          />

        {/* We need component to send saved data to backend */}
        <button className="btn-main"> Save </button>
        </form>
        </label>
      </div>

    
      <div className="minibox"> 
        <label className="custom-field-settings"> 
            <h2> Personal Detials </h2>
            <form> 
            <p> Legal name</p>
            <input
            type="text"
            /> 
            <p> Date of Birth </p> 
            {/* https://bootsnipp.com/snippets/MaKa3 */}
            <p> Scrollable Dropdown Menu </p> 
            <p> Street Address </p>
            <input/>

            <p> Unit#</p>
            <input/>

            <p> City/town </p> <p> State</p>
            <input/>
            <input/>

            <p> Postal Code </p> <p> Country </p>
            <input/>
            <input/>
            {/* We need component to send saved data to backend */}
            <button> Save </button>
            </form>

            </label>
          </div>
        </div>
    </div>
       
    )
}

export default Settings
