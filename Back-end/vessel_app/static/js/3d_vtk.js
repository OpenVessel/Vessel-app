/* We will grab a .VTK source and use filters to edit it 
Then we will map it which will turn it into a renderable object
An actor object will 'emulate' it and it can be displayed by Vtk Render window
*/
import vtkVolume from 'vtk.js/Sources/Rendering/Core/Volume';
import vtkVolumeMapper from 'vtk.js/Sources/Rendering/Core/VolumeMapper';
import vtkXMLImageDataReader from 'vtk.js/Sources/IO/XML/XMLImageDataReader';

import vtkGenericRenderWindow from 'vtk.js/Sources/Rendering/Misc/GenericRenderWindow';

//import vtkFullScreenRenderWindow from 'vtk.js/Sources/Rendering/Misc/FullScreenRenderWindow';
// Post-Processing / filter
import vtkPiecewiseFunction from 'vtk.js/Sources/Common/DataModel/PiecewiseFunction';
import vtkColorMaps from 'vtk.js/Sources/Rendering/Core/ColorTransferFunction/ColorMaps';
import vtkColorTransferFunction from 'vtk.js/Sources/Rendering/Core/ColorTransferFunction';

export function importVTK(){
    // -- setting up renderer --
    const container = document.querySelector('#container');

// We use the wrapper here to abstract out manual RenderWindow/Renderer/OpenGLRenderWindow setup
    const genericRenderWindow = vtkGenericRenderWindow.newInstance();
    genericRenderWindow.setContainer(container);
    genericRenderWindow.resize();

    const renderer = genericRenderWindow.getRenderer();
    const renderWindow = genericRenderWindow.getRenderWindow();

    // -- setting up volume actor & mapper --
    const actor = vtkVolume.newInstance();
    const mapper = vtkVolumeMapper.newInstance();
    //wiring the reader into the mapper into the actor 
    actor.setMapper(mapper);
    // -- setting up mutator --
    
    const lookupTable = vtkColorTransferFunction.newInstance();
    const piecewiseFun = vtkPiecewiseFunction.newInstance();
    // set up color transfer function
    lookupTable.applyColorMap(vtkColorMaps.getPresetByName('Cool to Warm'));
    // hardcode an initial mapping range here.
    // Normally you would instead use the range from
    // imageData.getPointData().getScalars().getRange()
    lookupTable.setMappingRange(0, 256);
    lookupTable.updateRange();
    // set up simple linear opacity function
    // This assumes a data range of 0 -> 256
    for (let i = 0; i <= 8; i++) {
        piecewiseFun.addPoint(i * 32, i / 8);
    }
    // -- set the actor properties --
    actor.getProperty().setRGBTransferFunction(0, lookupTable);
    actor.getProperty().setScalarOpacity(0, piecewiseFun);
    // -- server request and rendering --
    const reader = vtkXMLImageDataReader.newInstance();
    mapper.setInputConnection(reader.getOutputPort());
    reader.setUrl('https://kitware.github.io/vtk-js-datasets/data/vti/LIDC2.vti')
        .then(() => reader.loadData())
        .then(() =>{
            // configuring the renderer
            renderer.addVolume(actor);
            // update lookup table mapping range based on input dataset
            const range = reader.getOutputData().getPointData().getScalars().getRange();
            lookupTable.setMappingRange(...range);
            lookupTable.updateRange();
            // rendering
            renderer.resetCamera();
            renderWindow.render();
    });
}
