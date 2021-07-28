import React, { useState, useEffect } from "react";
import getState from "./flux.js";

// ERRORs
//× TypeError: Cannot read property 'value' of undefined
// Don't change, here is where we initialize our context, by default it's just going to be null.
export const Context = React.createContext(null);
// This function injects the global store to any view/component where you want to use it, we will inject the context to layout.js, you can see it here:
// https://github.com/4GeeksAcademy/react-hello-webapp/blob/master/src/js/layout.js#L35
const injectContext = PassedComponent => {
	const StoreWrapper = props => {
		//this will be passed as the contenxt value
		const [state, setState] = useState(
			getState({
				getStore: () => state.store,
				getActions: () => state.actions,
				setStore: updatedStore =>
					setState({
						store: Object.assign(state.store, updatedStore),
						actions: { ...state.actions }
					})
			})
		);

		// useEffect is for side-effect independent of rendering
		// useEffect(callback[, dependencies]); callback is function side-effect logic and dependencies is state 
		// useEffect explaination https://dmitripavlutin.com/react-useeffect-explanation/
		// useEffect https://dmitripavlutin.com/react-useeffect-infinite-loop/
		useEffect(() => {
			/**
			 * EDIT THIS!
			 * This function is the equivalent to "window.onLoad", it only runs once on the entire application lifetime
			 * you should do your ajax requests or fetch api requests here. Do not use setState() to save data in the
			 * store, instead use actions, like this:
			 **/
			// state.actions.getMessage(); // <---- calling this function from the flux.js actions
			state.actions.csrf_token_call(); // this calls 
			state.actions.syncTokenFromSessionStore();

		}, []); // so state(dependencies) to control whne the side-effect to run we are synctoken everytime state

		// The initial value for the context is not null anymore, but the current state of this component,
		// the context will now have a getStore, getActions and setStore functions available, because they were declared
		// on the state of this component
		return (
			<Context.Provider value={state}>
				<PassedComponent {...props} />
			</Context.Provider>
		);
	};
	return StoreWrapper;
};

export default injectContext;