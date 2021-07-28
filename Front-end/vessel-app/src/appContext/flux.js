const getState = ({ getStore, getActions, setStore }) => {
	const domainUrl = 'http://127.0.0.1:5000';

	return {
		//store local session?
		store: {
			token: null,
			csrf_token:null,
			token_id:null,
			message: null,
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
					setStore({ csrf_token: data.data, token_id: data.token_id});
					// console.log(csrf_token)
					
					// call this if statement after the token has been put into session
					// if(csrf_token && csrf_token !== "" && csrf_token !== undefined) setStore({ csrf_token: data.data});
					
					return true;
		
				}
				catch(error){
					console.error("There has been an error with inital_csrf_token");
				}


				// let parsedResponse = fetchGetResponse.json();
				// const csrf_token = sessionStorage.getItem("csrf_token");

				// console.log("Hello ", parsedResponse)
				// if(csrf_token && csrf_token !== "" && csrf_token !== undefined) setStore({ csrf_token: csrf_token});

			},

			
			logout: () => {
				sessionStorage.removeItem("token"); // takes token from session storage and stores it in the store
				console.log("Logging Out")
				setStore({ token:null });
				
			},

			// action login
			//
			login: async (email, password) => {
				const opts = { 
					method:'POST',
					headers:{
						"Content-Type":"application/json"
					},
					body: JSON.stringify({
						"email":email,
						"password": password 
					})
				};
				// basically were fetching api of production server
				// {ip/api/token}
				// api demo.openvessel.org
				try{
					const resp = await fetch('http://127.0.0.1:5000/api/token', opts)
					if(resp.status !== 200){
						alert("There has been some error");
						return false;
					}

					const data = await resp.json();
					console.log("this came from the backend", data);
					sessionStorage.setItem("token", data.access_token);
					setStore({token: data.access_token}); //setStore login view refresh its hooked to COntext
					return true;
		
				}
				catch(error){
					console.error("There has been an error with login");
				}
			},

			registration: async (token_id, csrf_token, username, email, password, confirmpassword) => {
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
					// sessionStorage.setItem("token", data.access_token);
					// setStore({token: data.access_token}); //setStore login view refresh its hooked to COntext
					return true;
		
				}
				catch(error){
					console.error("There has been an error with login");
				}
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