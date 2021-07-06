import React from 'react';
import "../css/dropzone.css"

const DropZone = () => {
    return (
<div> 
<h1> Drag & Drop files here or click to upload</h1>
<div className="container">
    <div className="drop-container">
        <div className="drop-message">
        <div className="upload-icon"></div>
        Drag & Drop files here or click to upload
        </div>
    </div>
</div>
</div>
    )
}
export default DropZone;