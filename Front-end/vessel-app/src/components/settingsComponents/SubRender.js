import React from 'react'
import SubNavBar from './SubNavBar'
import Settings from './Settings'
import Preferences from './Preferences'
import FinancialServicies from './FinancialServicies'
import AccountLevels from './AccountLevels'
import PrivacyRights from './PrivacyRights'
import LinkedAccounts from './LinkedAccounts'
import CryptoAddress from './CryptoAddress'

class SubRender extends React.Component {
    
    render(){ 
    if(this.props.localurl ==='/settings'){
        return (
            
        <div>
            <div className="row card SubNavStyle">
            <SubNavBar/>
            <p> {this.props.localurl}</p>
            <Settings/>

            </div>
        </div>
        )
    }
    if(this.props.localurl ==='/'){
        return (
            
        <div>
            <div className="row card SubNavStyle">
            <SubNavBar/>
            <p> {this.props.localurl}</p>
            <Settings/>

            </div>
        </div>
        )
    }
    if(this.props.localurl ==='/account-levels'){
        return (
            
        <div>
            <div className="row card SubNavStyle">
            <SubNavBar/>
            <p> {this.props.localurl}</p>
            <AccountLevels/>
            </div>
        </div>
        )
    }
    if(this.props.localurl ==='/preferences'){
        return (
            
        <div>
            <div className="row card SubNavStyle">
            <SubNavBar/>
            <p> {this.props.localurl}</p>
            <Preferences/>
            </div>
        </div>
        )
    }
    if(this.props.localurl ==='/Financial-services'){
        return (
            
        <div>
            <div className="row card SubNavStyle">
            <SubNavBar/>
            <p> {this.props.localurl}</p>
            <FinancialServicies/>
            </div>
        </div>
        )
    }
    if(this.props.localurl ==='/privacy-rights'){
        return (
            
        <div>
            <div className="row card SubNavStyle">
            <SubNavBar/>
            <p> {this.props.localurl}</p>
            <PrivacyRights/>
            </div>
        </div>
        )
    }
    if(this.props.localurl ==='/Linked-accounts'){
        return (
            
        <div>
            <div className="row card SubNavStyle">
            <SubNavBar/>
            <p> {this.props.localurl}</p>
            <LinkedAccounts/>
            </div>
        </div>
        )
    }
    if(this.props.localurl ==='/crypto-address'){
        return (
            
        <div>
            <div className="row card SubNavStyle">
            <SubNavBar/>
            <p> {this.props.localurl}</p>
            <CryptoAddress/>
            </div>
        </div>
        )
    }
    
    }
}
export default SubRender