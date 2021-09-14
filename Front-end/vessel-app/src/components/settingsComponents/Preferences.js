import React from 'react'

const Preferences = () => {
    return (
        <div>
            <div className="account-section">
            <h2> Preferences</h2>

            <p> Local currency Drop Down</p>
            <p> Time Zone Drop Down </p>

            {/* we need a save component */}
            <button> Save </button>

            </div>
        </div>
    )
}

export default Preferences
