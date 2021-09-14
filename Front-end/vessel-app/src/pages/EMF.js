import React, {useContext} from 'react'
import ProgressBar from '../components/ProgressBar'
import Deposit from '../components/Deposit'
import {Context} from "../appContext/UserContext"
const EMF = () => {

    
    const{store, actions } = useContext(Context);   
    return (
        <div>
            <div className="row"> 
            <div className="eleven column">
            <div className="card_page"> 
            <h5> Emergency Medical Fund </h5>

            <ProgressBar/>
            <Deposit> </Deposit>
            </div>
            </div>
            </div>
        </div>
    )
}

export default EMF
