// entry point of the application for building bundle.js (see webpack.config.js)
import React from 'react';
import ReactDOM from 'react-dom';
import routes from "./routes";

ReactDOM.render(routes, document.getElementById("container"));