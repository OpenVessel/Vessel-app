import React, {useContext, useState} from 'react'
import DropZone from '../components/DropZone.js';
import {Context} from "../appContext/UserContext"
const Upload = () => {
    const {store, actions} = useContext(Context);
    const [image, setImage] = useState("");

    let userName = window.sessionStorage.getItem("username")
    const fileSelectedHandler = event => { 
        console.log(event.target.files[0]);
        // muiltfile input is possible 

        setImage( event.target.files[0])

    }

    const fileUploadHandler = () => { 
        console.log("test")

        if(image === '' || image === undefined || image === null) { 
            console.log("You did not upload a file")
        }else{

        actions.UploadImages(
            store.token_id, 
            store.csrf_token,
            userName,
            image
            )
        }
    }
    
    return (
        <div>
        <div className="card_page"> 
            <div className="minibox"> 
            <h2 > Drag & Drop Medical bills </h2>
            <input type="file" onChange={fileSelectedHandler}/>
            </div>

            <div className="minibox"> 
            <p> The size of the claim </p>
            <input type="number"/> 

            <p> The bill its from hospital </p>
            <input type="text"/> 
            

            <button className="btn-main" onClick={fileUploadHandler}> Submit Claim</button>
            </div>
            
        </div>
        </div>
    )
}

export default Upload
// D:\L_pipe\vessel_app_celery\Vessel-app\Front-end\vessel-app\src\components\DropZone.js
//import Card from './components/Card'
// HOC Higher Order Components conditional rendering

// Listen for drag and drop
// Detect when a file is dropped on the drop zone
// Display image name and file type
// Validate dropped images
// Delete images with unsupported file types
// Preview images with valid file types
// Upload images
