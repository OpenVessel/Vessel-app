import React from 'react'
import DropZone from '../components/DropZone.js';
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

const Upload = () => {
    
    const fileSelectedHandler = event => { 
        console.log(event);
    }
    
    return (
        <div>
        <p className="title"> Drag & Drop Medical bills </p>
        <input type="file" onChange={fileSelectedHandler}/>
        </div>
    )
}

export default Upload
