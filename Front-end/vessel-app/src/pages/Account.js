import React, {useContext, useState} from 'react'
import {Context} from "../appContext/UserContext"
import profileImg from '../images/default_user.png'

const Account = () => {
      
  const{store, actions } = useContext(Context);
  const[email, setEmail] = useState("");
  const Webpage = 'Account'
  const username = store.username
  const DisplayEmail = store.email

  const [image, setImage] = useState({ preview: profileImg, raw: "" });

  const handleChange = e => {
    console.log(e.target.files[0]);
    if (e.target.files.length) {
      setImage({
        preview: URL.createObjectURL(e.target.files[0]),
        raw: e.target.files[0]
      });
    }
  };


  // const handleUpload = async e => {
  //   e.preventDefault();
  //   const formData = new FormData();
  //   formData.append("image", image.raw);
  //   return formData
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
        
        <div className="row card">
        <div className="account-section">
            <div className="one columns"></div>
            <div className="ten columns ">
            <div style={{float : 'center', paddingRight : '5px'}}>
            <img className="rounded-circle account-img" src={profileImg} alt='Account Image' style={{width:"250px", height:"250px"}}/>
                <h2  id='username-text'>{username }</h2>
                <p  id='email-text'>{ DisplayEmail }</p>
            </div>
        </div>
        <div className="one columns"></div>
        
      {/* ACCOUNT INFO */}
      
      <form method="POST" action="" encType="multipart/form-data">
        <input id="csrf_token" name="csrf_token" type="hidden" value={store.token} />
        <fieldset className="form-group">
          <legend className="border-bottom mb-4">Account info</legend>
          {/* EMAIL */}
          <div className="form-group account-form" id="email-field">
            <label className="form-control-label" htmlFor="email">Email</label>
            <input type="text"  placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            {/* <input className="form-control form-control-lg" id="email" name="email" required type="text" defaultValue={store.email}  /> */}
          </div>
          {/* IMAGE UPLOAD */}
          <div className="form-group account-form" id="image-upload">
        
          <label htmlFor="upload-button">
        {image.preview ? (
          <>
          <div className="form-group account-form" id="image-upload">
          <p> Click the Preview Image Below to upload a new profilo Picture</p>
          <img src={image.preview} alt="dummy" className="photo"/>
          </div>
          </>
        ) : (
          <>
            <span className="fa-stack fa-2x mt-3 mb-2">
              <i className="fas fa-circle fa-stack-2x" />
              <i className="fas fa-store fa-stack-1x fa-inverse" />
            </span>
            <h2 className="text-center">Upload your photo</h2>
          </>
        )}
      </label>
      <input
        type="file"
        id="upload-button"
        style={{ display: "none" }}
        onChange={handleChange}
      />
          </div>

      
        </fieldset>
        <div className="form-group account-form">
          <button className="btn-main" id="submit" name="submit" type="submit" onClick={handleClick} > Update Account Information </button>
        </div>
      </form>
        
        
        
        </div>
    </div>


</div>
    )
}

export default Account
