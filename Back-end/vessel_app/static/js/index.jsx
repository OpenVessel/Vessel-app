// render stuf here
// import React from 'react';
// import ReactDOM from 'react-dom';
// import Home from "./components/Home";
// import VTK from "./components/Vtk_view-port";
import {importVTK} from './3d_vtk'

//var line = <Home/> 
//var line2 = <VTK/>

//ReactDOM.render(line, document.getElementById("content"));
//ReactDOM.render(line2, document.getElementById("container"));
var path = document.getElementById("vti-path-holder").getAttribute("value");
importVTK(path);