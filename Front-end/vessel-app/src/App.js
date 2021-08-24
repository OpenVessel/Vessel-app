// import logo from './logo.svg';
// import './App.css';
import React from 'react';
import Layout from './components/Layout';

// import react-router
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";

// All webpages
import Login from './pages/Login'
import Home from './pages/Home'
import GettingStarted from './pages/Getting_Started'
import pnf from './pages/page_not_found'
import Upload from './pages/Upload'
import Browser from './pages/Browser'
import Account from './pages/Account'
import Register from './pages/Register'
import ContactInfo from './pages/ContactInfo'
import IdVerification  from './pages/IdVerification'
import injectContext from './appContext/UserContext';

import "./css/theme_skeleton.css"
import "./css/normalize.css"

// JSX javascript exetension
function App() {

// useState example through useContext passing
// const [user_value, setValue] = useState('hello from context')
// // useMemo obverse state changes
// const providerValue = useMemo(() => ({user_value, setValue}), [user_value, setValue]);
// console.log(providerValue)


// we defined react routes below
//implementation of react router
//https://reactrouter.com/web/guides/primary-components
//https://www.youtube.com/watch?v=o__czqXJtqk&ab_channel=PedroTech
//https://medium.com/javascript-scene/the-missing-introduction-to-react-62837cb2fd76

// initalize used state, state is something inside of compoenent 
// state is used when a user has done a action and then causes the application to rerender

//isLoggedIn is default false // we check inside the layout if


  return (
    <div className="App">
      {/* Layout is the navbar plus footer */}

      <Router>
      
        <Layout title='OpenVessel' /> 
        
          <Switch> 
          
          <Route path="/" exact component={Home}/>
          <Route path="/login" exact component={Login}/>
          <Route path="/getting_started" exact component={GettingStarted}/>
          <Route path="/upload" exact component={Upload}/>
          <Route path="/browser" exact component={Browser}/>
          <Route path="/account" exact component={Account}/>
          <Route path="/register" exact component={Register}/>
          <Route path="/ContactInfo" exact component={ContactInfo}/>
          <Route path="/IdVerification" exact component={IdVerification}/>


          <Route path="*" exact component={pnf}/>
          </Switch>
          
        </Router>
    </div>
  );

}

export default injectContext(App);
