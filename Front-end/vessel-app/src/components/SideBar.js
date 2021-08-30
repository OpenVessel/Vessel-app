import React from 'react';
// class SideBarWelcome extends React.Component
class SideBar extends React.Component {
    render(){ 
        console.log(this.props.title)
    if(this.props.title ==='Register'){
        return ( 
            <div>
                <div className="SideBar">
                        <div className="row outer-row">
                            <h6> Out-of-Pocket Insurance Premium </h6>
                            <p> 
                            Make monthly payments of low-end $150 to pay off any
                            medical bills with small to large ducbuitles debt. 
                            To high-end of premium of $300. 
                            </p>
    
                            <h6> Premium with Interest</h6>
                            <p> After 6 months of paying Premiums you are allowed to 
                            withdraw your contributions in total but with contiuned contributions 
                            start building interest and increases with subsequent contributions.
                            </p>
                    </div>
                </div>
            </div>
            );
        } 
        if(this.props.title === 'ContactInfo'){ 
            return( 
            <div>
                <div className="SideBar">
                        <div className="row outer-row">
                            <h6> Why does OpenVessel need my address? </h6>
                            <p> 
                            The US Government requires all finanical business, including OpenVessel, 
                            to collect your address for identity Verification.
                            Read more here.
                            </p>
    
                            <h6> Will OpenVessel send mail, advertisements, or 
                            phone calls to your address or phone number?</h6>
                            <p> 
                            No. We will not send you advertisements, or call you directly. 
                            We strictly use it for identity Verification. 
                            </p>
                    </div>
                </div>
            </div>
        );

        }
        
        if(this.props.title === 'Verification'){ 
            return( 
            <div>
                <div className="SideBar">
                        <div className="row outer-row">
                            <h5> Test </h5>
                            <p> 
                            Make monthly payments of low-end $150 to pay off any
                            medical bills with small to large ducbuitles debt. 
                            To high-end of $300. 
                            </p>
                    </div>
                </div>
            </div>
        );

        }


    return null;
    
    }
    
}

export default SideBar