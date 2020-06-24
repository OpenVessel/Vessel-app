import React, { Component } from 'react';
import macro from 'vtk.js/Sources/macro'

console.log('vtk.js imported: ', macro)


export default class VTK extends Component {
    render() {
       return (
          <h1>Hello React!</h1>
       )
    }
}

