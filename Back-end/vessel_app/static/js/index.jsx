// render stuf here
import React from 'react';
import ReactDOM from 'react-dom';
import Home from "./components/Home";
import VTK from "./components/Vtk_view-port";

var line = <Home/> 
var line2 = <VTK/>
ReactDOM.render(line, document.getElementById("content"));
ReactDOM.render(line2, document.getElementById("container"));