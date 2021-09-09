import React from 'react'
import CoverageBar from '../components/ProgressBarCoverage'
import UploadSection from '../components/UploadSection'
import RenderUpload from '../components/RenderUpload'
const Browser = () => {

    // were going to pass user store-id and context to send web request 

    return (
        <div>
            {/* Graph or progress bar represent the amount of money */}
            <CoverageBar> 

            </CoverageBar>
            {/* Upload feature for medical bills (greyed out if not validaited, or pay any money ) */}
            <UploadSection>

            </UploadSection> 
            {/* Browser all uploads below */}
            <RenderUpload>
                
            </RenderUpload> 
        </div>
    )
}

export default Browser
