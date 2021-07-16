const getState = ({ getStore, getActions, setStore }) => {
	return {
		//store local session?
		store: {
			token: null,
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

			registration: async (csrf_token, username, email, password, confirmpassword) => {
				const opts = { 
					method:'POST',
					headers:{
						"Content-Type":"application/json"
					},
					body: JSON.stringify({
						"csrf_token":csrf_token,
						"username":username,
						"email":email,
						"password": password,
						"confirmpassword":confirmpassword,
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