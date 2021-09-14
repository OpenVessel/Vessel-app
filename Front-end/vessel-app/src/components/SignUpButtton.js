import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Link, Redirect} from "react-router-dom";

class ChangeInput extends Component {
    

    handleEvent = event => {
    
    console.log("handles work?")
    console.log( "State condition" , this.props.moveOn)
    if( this.props.moveOn == true){ 
    console.log("test")
    // return <Redirect to={this.state.redirect} />
        setTimeout(function(){
            const WorkPlz = true    
    }, 2000);//wait 2 seconds
    }
    };
  render() {
    if (this.WorkPlz) {
        return <Redirect to={"/contactInfo"} />
      }
      return(
        <button  className='btn-main form-input-btn' type='submit' onClick={this.handleEvent}>
        Sign Up
     </button>
      )
    }
}

export default ChangeInput;