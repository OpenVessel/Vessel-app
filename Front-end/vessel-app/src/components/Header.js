import Button from './Button'
import {Link} from "react-router-dom";


const Header = (props) => {
    // Header contain if statement for user authentication 
    // to determine to show user specific page or not check cite
    //https://reactjs.org/docs/conditional-rendering.html
    console.log(props.isLoggedIn === true)
    console.log(props.isLoggedIn)
    if (props.isLoggedIn === true) {
        return <UserIsLoggedIN props />;
      }
      return <UserLoggedOut props />;
    }

// rafce 
// apply conditional Rendering
// 6/7/2021

const onClick = (e) => { 
    console.log('click')
}


function UserIsLoggedIN(props) {
    
    console.log("User Logged In")
    return (
        <header className='header'>
            
            {/* if user is authenticated */}
            <Link to="/"> Home </Link>
            <Button onClick={onClick} text='Browser'> </Button>
            <Button text='Getting Started'> </Button>
            <Button text='Upload'> </Button>
            <Button text='Account'> </Button>
            <Button text='Log out'> </Button>
        </header>
    )
  }
  
  function UserLoggedOut(props) {
    console.log("User Logged Out")
    return (
        <header className='header'>
            <h1 style ={headingStyle}>{props.title} </h1>
            
            {/* else  */}
            <Link to="/"> Home </Link>
            <Link to="/Getting_Started"> Getting Started </Link>
            
            
            {/* <Button onClick={onClick} text='Home'> </Button>
            <Button text='Getting Started'> </Button>

            <Button text='Login'> </Button> */}
        </header>
    )
  }
  


export default Header

