import React from 'react';
import { BrowserRouter, Route, browserHistory } from 'react-router-dom';
import VTIViewer from './components/vtk-volume-viewer';


export default (
    <BrowserRouter history={browserHistory}>
    <div>
        <Route path='/3d_viewer' render={() => (
            <VTIViewer path={document.querySelector("#vti-path-holder").getAttribute("value")} 
                container={document.querySelector("#vtk-container")}/>
        )}/>
    </div>
    </BrowserRouter>
);