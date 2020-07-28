/* We will grab a .VTK source and use filters to edit it 
Then we will map it which will turn it into a renderable object
An actor object will 'emulate' it and it can be displayed by Vtk Render window
*/

import vtkVolume from 'vtk.js/Sources/Rendering/Core/Volume';
import vtkVolumeMapper from 'vtk.js/Sources/Rendering/Core/VolumeMapper';
import vtkXMLImageDataReader from 'vtk.js/Sources/IO/XML/XMLImageDataReader';
import vtkGenericRenderWindow from 'vtk.js/Sources/Rendering/Misc/GenericRenderWindow';

// Post-Processing / filter
import vtkBoundingBox from 'vtk.js/Sources/Common/DataModel/BoundingBox';
import vtkPiecewiseFunction from 'vtk.js/Sources/Common/DataModel/PiecewiseFunction';
import vtkVolumeController from 'vtk.js/Sources/Interaction/UI/VolumeController';
import vtkColorTransferFunction from 'vtk.js/Sources/Rendering/Core/ColorTransferFunction';
import vtkColorMaps from 'vtk.js/Sources/Rendering/Core/ColorTransferFunction/ColorMaps';


export function importVTK(path){   

    //testing github
    // Setting up viewport container
    const rootContainer = document.querySelector(
        '#container'
    ); 

    const genericRenderer = vtkGenericRenderWindow.newInstance({
        background: [0, 0, 0],
        rootContainer,
    });
    genericRenderer.setContainer(rootContainer);
    genericRenderer.resize();
    const renderWindow = genericRenderer.getRenderWindow();
    const renderer = genericRenderer.getRenderer();
    

    renderWindow.getInteractor().setDesiredUpdateRate(15.0);
    
    const body = document.querySelector('#container');

    // Create Widget container
    const widgetContainer = document.createElement('div');
    widgetContainer.style.position = 'absolute';
    widgetContainer.style.top = 'calc(10px + 1em)';
    widgetContainer.style.left = '5px';
    widgetContainer.style.background = 'rgba(255, 255, 255, 0.3)';
    body.appendChild(widgetContainer);    
    
    // ------------------------ FUNCTIONALITY -------------------------------
    
    const globalDataRange = [0, 255];

    // -- setting up volume actor & mapper --
    const actor = vtkVolume.newInstance();
    const mapper = vtkVolumeMapper.newInstance({ sampleDistance: 1.1 });

    // -- setting up mutator --
    
    const lookupTable = vtkColorTransferFunction.newInstance();
    
    // set up color transfer function
    lookupTable.applyColorMap(vtkColorMaps.getPresetByName('erdc_rainbow_bright'));
    // changable mapping range that will be updated by widget i think
    lookupTable.setMappingRange(...globalDataRange);
    lookupTable.updateRange();

    
    const piecewiseFunction = vtkPiecewiseFunction.newInstance();

    // -- server request and rendering --
    const reader = vtkXMLImageDataReader.newInstance();
    mapper.setInputConnection(reader.getOutputPort());


    
    // ---------- Actual Loading and Rendering -------
    reader.setUrl(path)
        .then(() => reader.loadData())
        .then(() =>{    
            // processsing image data to be displayed nicely
            const imageData = reader.getOutputData(0);
            
            console.log(imageData);
            const dataArray = imageData.getPointData().getScalars() || imageData.getPointData().getArrays()[0];            ;
            const dataRange = dataArray.getRange();
            
            globalDataRange[0] = dataRange[0];
            globalDataRange[1] = dataRange[1];
            
            actor.setMapper(mapper);
            mapper.setInputData(imageData);
            renderer.addVolume(actor);

            const sampleDistance =
            0.7 *
            Math.sqrt(
                imageData
                .getSpacing()
                .map((v) => v * v)
                .reduce((a, b) => a + b, 0)
            );
            mapper.setSampleDistance(sampleDistance);

            // ------  CONFIGUREING ACTOR ---------------
   
            actor.getProperty().setRGBTransferFunction(0, lookupTable);
            actor.getProperty().setScalarOpacity(0, piecewiseFunction);
            // actor.getProperty().setInterpolationTypeToFastLinear();
            actor.getProperty().setInterpolationTypeToLinear();
            // For better rendering
            actor
            .getProperty()
            .setScalarOpacityUnitDistance(
            0,
            vtkBoundingBox.getDiagonalLength(imageData.getBounds()) /
                Math.max(...imageData.getDimensions())
            );
            // boundariy something
            actor.getProperty().setGradientOpacityMinimumValue(0, 0);
            actor
                .getProperty()
                .setGradientOpacityMaximumValue(0, (dataRange[1] - dataRange[0]) * 0.05);
            actor.getProperty().setShade(true);
            actor.getProperty().setUseGradientOpacity(0, true);
            actor.getProperty().setGradientOpacityMinimumOpacity(0, 0.0);
            actor.getProperty().setGradientOpacityMaximumOpacity(0, 1.0);
            actor.getProperty().setAmbient(0.2);
            actor.getProperty().setDiffuse(0.7);
            actor.getProperty().setSpecular(0.3);
            actor.getProperty().setSpecularPower(8.0);
            
            // ------  CONFIGUREING WIDGET ---------------

            const widget = vtkVolumeController.newInstance({
                size: [400, 150],
                rescaleColorMap: true,
            });
            widget.setContainer(widgetContainer);
            widget.setupContent(renderWindow, actor, true/*is background dark?*/);
            // setUpContent above sets the size to the container.
            // We need to set the size after that.
            // controllerWidget.setExpanded(false);
            
            // Basic size maybe change?
            widget.setSize(400, 150);

            // rendering
            widget.render();

            renderer.resetCamera();
            renderer.getActiveCamera().elevation(70);
            renderWindow.render();
    });
}





