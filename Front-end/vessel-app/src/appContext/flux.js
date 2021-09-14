import React from 'react'
import  { Redirect} from 'react-router-dom'

const getState = ({ getStore, getActions, setStore }) => {
	const domainUrl = 'http://127.0.0.1:5000';

	function resolveAfterTime(callback, time, msg) {
		new Promise(resolve => {
			setTimeout(() => {
				resolve(msg);

			}, time);
		}); 
		setTimeout(() => {
			callback(msg);
		}, 1500);
		return msg
		
	}

	// function imageDatatoBlob(image_data, value){
	// 	return new Promise(function(resolve, reject){
	// 	  // const obj = { hello: medical_data }
	// 	  // const blob = new Blob([JSON.stringify(obj)], {type : 'application/json'})
	// 	  const blob = new Blob([JSON.stringify(image_data)], {type : 'application/json'})
	// 	resolve(Blob)
	// 	});
	// }

		//redirect with js or "middleware"
	function redirectLogic(msg){
		console.log("----", msg)
		console.log(msg === 'Your account has been created! You are now able to log in')
		console.log(msg ==='Failed to commit data to the database')
		if(msg ==='Failed to commit data to the database'){
			console.log("failed to commit" )
		}
		
		if( msg === 'Your account has been created! You are now able to log in'){

		console.log("Redirecting")
		window.location.replace("http://localhost:3000/contactInfo") // replace URL from .env
		return <Redirect to='/contactInfo'  />
		
		} else {
		console.log("Failed Registertion see msg")
		return msg
		}

	}

	return {
		//store local session?
		store: {
			token: null,
			csrf_token:null,
			token_id:null,
			message: null,
			email:null, 
			username:null,
			return_msg:null,
			firstname:null,
			plaidToken:null,
			
			VerificationStatus: [{
				username:null,
				userMade:null,
				userContactInfo:null,
				userVerify:null, 
			}],

			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			]
		},
		actions: {
			// Use getActions to call a function within a fuction //action called 
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},

			syncTokenFromSessionStore: () => {
				const token = sessionStorage.getItem("token"); // takes token from session storage and stores it in the store
				console.log("Application just loaded, synching the session storage token")
				if(token && token !== "" && token !== undefined) setStore({ token: token});
				
			},

			// Global session call to GET csrf_token from flask and store in session
			csrf_token_call: async () => {
				// csrfTokenState set to default
				const url = '/api/csrf_token_call';
				// const data = 'A$1;,BOimZ7i+_t**]Nq3El)!#bG|K'
				let fetchGetResponse = await fetch(`${domainUrl}${url}`, {
					method: 'GET',
					headers: {
						// Accept: "application/json",
						"Content-Type": "application/json",
						
					},
					credentials: "include",
					referrerPolicy: 'no-referrer',
					mode: 'cors',
					// body: data
				});
				
				try{
					const data = await fetchGetResponse.json();
					console.log("backend_csrf_token_for_single_user", data);
					// setStore({csrf_token: data.csrf_token}); //setStore login view refresh its hooked to COntext
					sessionStorage.setItem("csrf_token", data.data);
					sessionStorage.setItem("token_id", data.token_id);
					sessionStorage.setItem("return_msg",null)
					setStore({ csrf_token: data.data, token_id: data.token_id});
					// console.log(csrf_token)
					
					// call this if statement after the token has been put into session
					// if(csrf_token && csrf_token !== "" && csrf_token !== undefined) setStore({ csrf_token: data.data});
					
					return true;
		
				}
				catch(error){
					console.error("There has been an error with inital_csrf_token");
				}

			},

			VerificationCheck: async (token_id, csrf_token, username) => {
				const opts = { 
					method:'POST',
					headers:{
						"Content-Type":"application/json"
					},
					body: JSON.stringify({
						"token_id":token_id,
						"csrf_token":csrf_token,
						"username":username,					
						"submit":"VerificationCheck"
					})
				};
				// basically allowing the react user to register via API 
				try{
					const resp = await fetch('http://127.0.0.1:5000/api/verificationcheck', opts)
					if(resp.status !== 200){
						alert("There has been some error");
						return false;
					}

					const data = await resp.json();
					console.log("this came from the backend", data);
					sessionStorage.setItem("return_msg",data.return_msg)
					sessionStorage.setItem("username",data.username)
					sessionStorage.setItem("userMade",data.userMade)
					sessionStorage.setItem("userContactInfo",data.userContactInfo)
					sessionStorage.setItem("userVerify",data.userVerify)
					// setStore({return_msg: data.message, firstname:data.firstname, username:data.username});
					// setStore({VerificationStatus:[{
					// 	username:data.username,
					// 	userMade:data.userMade,
					// 	userContactInfo:data.userContactInfo,
					// 	userVerify:data.userVerify, 
					// }]})
					//setStore login view refresh its hooked to COntext
					return true;
		
				}
				catch(error){
					console.error("There has been an error with login");
				}
			},


			PlaidEntryPoint: async (token_id, csrf_token, username) => {
				// csrfTokenState set to default
				const url = '/api/PlaidEntryPoint';
				// const data = 'A$1;,BOimZ7i+_t**]Nq3El)!#bG|K'
				let fetchGetResponse = await fetch(`${domainUrl}${url}`, {
					method: 'POST',
					headers: {
						// Accept: "application/json",
						"Content-Type": "application/json",
						
					},
					credentials: "include",
					referrerPolicy: 'no-referrer',
					mode: 'cors',
					body: JSON.stringify({
						"token_id":token_id,
						"csrf_token":csrf_token,					
						"username":username
					})
				});
				
				try{
					const data = await fetchGetResponse.json();
					console.log("backend_csrf_token_for_single_user", data);
					// setStore({csrf_token: data.csrf_token}); //setStore login view refresh its hooked to COntext
					sessionStorage.setItem("plaidToken", data.plaidToken);
					setStore({  plaidToken: data.token_id});
					// console.log(csrf_token)
					
					// call this if statement after the token has been put into session
					// if(csrf_token && csrf_token !== "" && csrf_token !== undefined) setStore({ csrf_token: data.data});
					
					return true;
		
				}
				catch(error){
					console.error("There has been an error with PlaidEntryPoint");
				}

			},

			
			logout: () => {
				sessionStorage.removeItem("token"); // takes token from session storage and stores it in the store
				console.log("Logging Out")
				setStore({ token:null });
				sessionStorage.setItem("return_msg",null)
				sessionStorage.setItem("username",null)
				sessionStorage.setItem("userMade",null)
				sessionStorage.setItem("userContactInfo",null)
				sessionStorage.setItem("userVerify",null)

				
			},

			// action login
			//
			login: async (username, password) => {
				const opts = { 
					method:'POST',
					headers:{
						"Content-Type":"application/json"
					},
					body: JSON.stringify({
						"username": username,
						"password": password 
					})
				};
				// basically were fetching api of production server
				// {ip/api/token}
				// api demo.openvessel.org
				try{
					const resp = await fetch('http://127.0.0.1:5000/api/login_call', opts)
					if(resp.status !== 200){
						alert("There has been some error");
						return false;
					}

					const data = await resp.json();
					console.log("this came from the backend", data);
					sessionStorage.setItem("token", data.access_token);
					sessionStorage.setItem("username", data.username);
					sessionStorage.setItem("email", data.email);
					setStore({token: data.access_token, username: data.username, email: data.email }); 
					//setStore login view refresh its hooked to Context

					return true;
		
				}
				catch(error){
					console.error("There has been an error with login");
				}
			},

			registration: async (token_id, csrf_token, firstname, lastname, username, email, password, confirmpassword) => {
				const opts = { 
					method:'POST',
					headers:{
						"Content-Type":"application/json"
					},
					body: JSON.stringify({
						"token_id":token_id,
						"csrf_token":csrf_token,
						"firstname":firstname, 
						"lastname":lastname,						
						"username":username,
						"email":email,
						"password": password,
						"confirm_password":confirmpassword,
						"submit":"Register"
					})
				};
				// basically allowing the react user to register via API 
				try{
					const resp = await fetch('http://127.0.0.1:5000/api/register', opts)
					if(resp.status !== 200){
						alert("There has been some error");
						return false;
					}

					const data = await resp.json();
					console.log("this came from the backend", data);
					sessionStorage.setItem("return_msg", data.message);
					sessionStorage.setItem("firstname", data.firstname);
					sessionStorage.setItem("username", data.username);
					setStore({return_msg: data.message, firstname:data.firstname, username:data.username});
					//setStore login view refresh its hooked to COntext
					return true;
		
				}
				catch(error){
					console.error("There has been an error with login");
				}
			},

			contactinfo: async ( 
				token_id, 
				csrf_token, 
				phonenumber, 
				residentialaddress, 
				username,
				city, 
				zipcode, 
				state, 
				stateName, 
				routeName,
				townName, 
				countryName
				) => {
				const opts = { 
					method:'POST',
					headers:{
						"Content-Type":"application/json"
					},
					body: JSON.stringify({
						"token_id":token_id,
						"csrf_token":csrf_token,
						"phonenumber":phonenumber, 
						"residentialaddress":residentialaddress,						
						"username":username,
						"city":city,
						"zipcode": zipcode,
						"state": state,
						"stateName":stateName ,
						"routeName":routeName,
						"townName": townName,
						"countryName": countryName,
						"submit":"ContactInfo"
					})
				};
				// basically allowing the react user to register via API 
				try{
					const resp = await fetch('http://127.0.0.1:5000/api/contactInfo', opts)
					if(resp.status !== 200){
						alert("There has been some error");
						return false;
					}

					const data = await resp.json();
					console.log("this came from the backend", data);
					sessionStorage.setItem("return_msg", data.message);
					setStore({return_msg: data.message});

					return true;
		
				}
				catch(error){
					console.error("There has been an error with login");
				}
			},

			Verification: async ( token_id, csrf_token, username, ssn, DOB, citizenship) => {
				const opts = { 
					method:'POST',
					headers:{
						"Content-Type":"application/json"
					},
					body: JSON.stringify({
						"token_id":token_id,
						"csrf_token":csrf_token,
						"username":username,
						"ssn":ssn, 
						"DOB":DOB,						
						"citizenship":citizenship,						
						"submit":"Verification"
					})
				};
				// basically allowing the react user to register via API 
				try{
					const resp = await fetch('http://127.0.0.1:5000/api/Verification', opts)
					if(resp.status !== 200){
						alert("There has been some error");
						return false;
					}

					const data = await resp.json();
					console.log("this came from the backend", data);
					sessionStorage.setItem("return_msg", data.message);
					setStore({return_msg: data.message});

					return true;
		
				}
				catch(error){
					console.error("There has been an error with login");
				}
			},


			changeAccount: async (token_id, csrf_token, username, email, password, Webpage, image_data) => {
				console.log("testt change account")
				// const blob = imageDatatoBlob(image_data)
				const opts = { 
					method:'POST',
					headers:{
						"Content-Type":"application/json"
					},
					body: JSON.stringify({
						"token_id":token_id,
						"csrf_token":csrf_token,
						"username":username,
						"email":email,
						"password": password,
						"image_data":image_data,
						"submit": Webpage
					})
				};
				// basically allowing the react user to register via API 
				try{
					const resp = await fetch('http://127.0.0.1:5000/api/account', opts)
					if(resp.status !== 200){
						alert("There has been some error");
						return false;
					}

					const data = await resp.json();
					console.log("this came from the backend", data);
					sessionStorage.setItem("return_msg", data.message);
					setStore({return_msg: data.message}); //setStore login view refresh its hooked to COntext
					return true;
		
				}
				catch(error){
					console.error("There has been an error with login");
				}
			},

			// registration promises to return data it resolves or is error relate to network or lag
			// we going implement a promise so basically when a user submits reg data we are expecting a return reponse to move 
			// the user to the login 

			redirect: async (msg) => {
				console.log('calling');
				const time = 500 // wait 100 mil for a response from the back-end then we a sec for msg to return
				
				// how do we trigger a fuction to run until msg contains a string?
				var msgboon = await resolveAfterTime(redirectLogic, time, msg); //https://stackoverflow.com/questions/49774769/javascript-uncaught-syntaxerror-identifier-has-already-been-declared
				
				// we could implement call back on resolveAfterTime? https://www.youtube.com/watch?v=ZYb_ZU8LNxs&ab_channel=freeCodeCamp.org
				// by using callback we form a order between functions 
				// setTimeout(() => { 
				// redirectLogic(msg);
				// }, 2000);
				
				return msgboon

				// fetch("http://127.0.0.1:5000/api/hello", opts)
				// .then(resp => resp.json())
				// .then(data => setStore({ message: data.message }))
				// .catch(
					
				// 	error => console.log("Error loading message from backend", error)

				// ); //Unexpected token < in JSON at position 0

			},


			getMessage: () => {

				// to access jwt_required protected view you need to send in JWT with each request. 
				// Authorization: Bearer <access_token> https://flask-jwt-extended.readthedocs.io/en/stable/
				const store = getStore();
				const opts = {  
					headers: {
						"Authorization":"Bearer " + store.token
					}

				}					
				
				// fetching data from the backend
				//fetch(process.env.BACKEND_URL + "/api/hello")
				fetch("http://127.0.0.1:5000/api/hello", opts)
					.then(resp => resp.json())
					.then(data => setStore({ message: data.message }))
					.catch(
						
						error => console.log("Error loading message from backend", error)

					); //Unexpected token < in JSON at position 0

			},

			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			}
		}
	};
};

export default getState;