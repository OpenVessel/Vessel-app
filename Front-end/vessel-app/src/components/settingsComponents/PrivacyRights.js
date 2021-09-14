import React from 'react'

const PrivacyRights = () => {
    return (
        <div>
            <div className="account-section">

            <h2> Privacy options </h2>

            <h5> Request Data </h5>
            <p> Recevie a copy of personal data held by OpenVessel </p> 
            {/* component button */}
            <h5> Request Deletion of Data</h5>
            <p> Delete specific data or all of my data</p>

            <h5> Request Export of Data </h5>
            <p> Export of my data in machine-readable form </p> 

            <h5> Request Correction of Data </h5> 
            <p> Correct, modify, or complete Data </p>

            <h5> Manage Cookies</h5>
            <p> Preferences for cookies</p>

            </div>
        </div>
    )
}

export default PrivacyRights
