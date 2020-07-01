import React, { Component } from 'react';

import macro from 'vtk.js/Sources/macro'
import VtkViewport from 'react-vtkjs-viewport'

import {
    View2D,
    vtkInteractorStyleMPRWindowLevel,
    invertVolume,
  } from '@vtk-viewport';

import vtkHttpDataSetReader from 'vtk.js/Sources/IO/Core/HttpDataSetReader';
import vtkVolume from 'vtk.js/Sources/Rendering/Core/Volume';
import vtkVolumeMapper from 'vtk.js/Sources/Rendering/Core/VolumeMapper';

console.log('HELP ME')
console.log('vtk.js imported: ', macro)


export default class VTK extends Component {
    render() {
       return (
          <h1>Hello React!</h1>
       )
    }



}

