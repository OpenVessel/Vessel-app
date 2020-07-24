
import vtkVolume from 'vtk.js/Sources/Rendering/Core/Volume';
import vtkVolumeMapper from 'vtk.js/Sources/Rendering/Core/VolumeMapper';
import vtkXMLImageDataReader from 'vtk.js/Sources/IO/XML/XMLImageDataReader';
import vtkGenericRenderWindow from 'vtk.js/Sources/Rendering/Misc/GenericRenderWindow';
// Post-Processing / filter
import vtkPiecewiseFunction from 'vtk.js/Sources/Common/DataModel/PiecewiseFunction';
import vtkPiecewiseGaussianWidget from 'vtk.js/Sources/Interaction/Widgets/PiecewiseGaussianWidget';
import vtkColorTransferFunction from 'vtk.js/Sources/Rendering/Core/ColorTransferFunction';
import vtkColorMaps from 'vtk.js/Sources/Rendering/Core/ColorTransferFunction/ColorMaps';


// import vtkVolume from 'vtk.js/Sources/Rendering/Core/Volume';
// import vtkVolumeMapper from 'vtk.js/Sources/Rendering/Core/VolumeMapper';
// import vtkXMLImageDataReader from 'vtk.js/Sources/IO/XML/XMLImageDataReader';

// import vtkGenericRenderWindow from 'vtk.js/Sources/Rendering/Misc/GenericRenderWindow';
// import vtkHttpDataSetReader from 'vtk.js/Sources/IO/Core/HttpDataSetReader';
// //import vtkFullScreenRenderWindow from 'vtk.js/Sources/Rendering/Misc/FullScreenRenderWindow';
// // Post-Processing / filter
// import vtkPiecewiseFunction from 'vtk.js/Sources/Common/DataModel/PiecewiseFunction';
// import vtkColorMaps from 'vtk.js/Sources/Rendering/Core/ColorTransferFunction/ColorMaps';
// import vtkColorTransferFunction from 'vtk.js/Sources/Rendering/Core/ColorTransferFunction';

// export function importVTK(path){
//     // -- setting up renderer --
//     console.log(path)
//     //path = "../static/users_3d_objects/user_1/data_object.vti"
//     console.log(path)
//     const container = document.querySelector('#container');

// // We use the wrapper here to abstract out manual RenderWindow/Renderer/OpenGLRenderWindow setup
//     const genericRenderWindow = vtkGenericRenderWindow.newInstance();
//     genericRenderWindow.setContainer(container);
//     genericRenderWindow.resize();

//     const renderer = genericRenderWindow.getRenderer();
//     const renderWindow = genericRenderWindow.getRenderWindow();

//     // -- setting up volume actor & mapper --
//     const actor = vtkVolume.newInstance();
//     const mapper = vtkVolumeMapper.newInstance();
//     //wiring the reader into the mapper into the actor 
//     actor.setMapper(mapper);
//     // -- setting up mutator --
    
//     const lookupTable = vtkColorTransferFunction.newInstance();
//     const piecewiseFun = vtkPiecewiseFunction.newInstance();
//     // set up color transfer function
//     lookupTable.applyColorMap(vtkColorMaps.getPresetByName('Cool to Warm'));
//     // hardcode an initial mapping range here.
//     // Normally you would instead use the range from
//     // imageData.getPointData().getScalars().getRange()
//     lookupTable.setMappingRange(0, 256);
//     lookupTable.updateRange();
//     // set up simple linear opacity function
//     // This assumes a data range of 0 -> 256
//     for (let i = 0; i <= 8; i++) {
//         piecewiseFun.addPoint(i * 32, i / 8);
//     }
//     // -- set the actor properties --
//     actor.getProperty().setRGBTransferFunction(0, lookupTable);
//     actor.getProperty().setScalarOpacity(0, piecewiseFun);
//     // -- server request and rendering --

//     const data_reader = vtkHttpDataSetReader.newInstance();

//     // DATA READER
//     const reader = vtkXMLImageDataReader.newInstance();
//     mapper.setInputConnection(reader.getOutputPort());
//     reader.setUrl(path)
//         .then(() => reader.loadData())
//         .then(() =>{
//             // configuring the renderer
//             renderer.addVolume(actor);
//             // update lookup table mapping range based on input dataset
//             const range = reader.getOutputData().getPointData().getScalars().getRange();
//             lookupTable.setMappingRange(...range);
//             lookupTable.updateRange();
//             // rendering
//             renderer.resetCamera();
//             renderWindow.render();
//     });
// }



export function importVTK(path){   
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
    // Create Label for preset
    const labelContainer = document.createElement('div');
    labelContainer.style.position = 'absolute';
    labelContainer.style.top = '5px';
    labelContainer.style.left = '5px';
    labelContainer.style.width = '100%';
    labelContainer.style.color = 'white';
    labelContainer.style.textAlign = 'center';
    labelContainer.style.userSelect = 'none';
    labelContainer.style.cursor = 'pointer';
    body.appendChild(labelContainer);
    // Creating gaussian widget and touching it
    const widget = vtkPiecewiseGaussianWidget.newInstance({
        numberOfBins: 256,
        size: [400, 150],
    });
        widget.updateStyle({
        backgroundColor: 'rgba(255, 255, 255, 0.6)',
        histogramColor: 'rgba(100, 100, 100, 0.5)',
        strokeColor: 'rgb(0, 0, 0)',
        activeColor: 'rgb(255, 255, 255)',
        handleColor: 'rgb(50, 150, 50)',
        buttonDisableFillColor: 'rgba(255, 255, 255, 0.5)',
        buttonDisableStrokeColor: 'rgba(0, 0, 0, 0.5)',
        buttonStrokeColor: 'rgba(0, 0, 0, 1)',
        buttonFillColor: 'rgba(255, 255, 255, 1)',
        strokeWidth: 2,
        activeStrokeWidth: 3,
        buttonStrokeWidth: 1.5,
        handleWidth: 3,
        iconSize: 20, // Can be 0 if you want to remove buttons (dblClick for (+) / rightClick for (-))
        padding: 10,
    });
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
    //wiring the reader into the mapper into the actor 
    actor.setMapper(mapper);
    actor.getProperty().setRGBTransferFunction(0, lookupTable);
    actor.getProperty().setScalarOpacity(0, piecewiseFunction);
    // actor.getProperty().setInterpolationTypeToFastLinear();
    actor.getProperty().setInterpolationTypeToLinear();
    // ---------- Actual Loading and Rendering -------
    reader.setUrl(path)
        .then(() => reader.loadData())
        .then(() =>{    
            // processsing image data to be displayed nicely
            const imageData = reader.getOutputData();
            const dataArray = imageData.getPointData().getScalars();
            const dataRange = dataArray.getRange();
            globalDataRange[0] = dataRange[0];
            globalDataRange[1] = dataRange[1];

            widget.setDataArray(dataArray.getData());
            widget.applyOpacity(piecewiseFunction);

            
            // Either update when widget change or when color change
            widget.setColorTransferFunction(lookupTable);
            lookupTable.onModified(() => {
                widget.render();
                renderWindow.render();
            });
            const source = reader.getOutputData(0);
            // rendering
            renderer.addVolume(actor);
            renderer.resetCamera();
            renderer.getActiveCamera().elevation(70);
            renderWindow.render();
    });
    // ----------------------------------------------------------------------------
    // Default setting Piecewise function widget
    // ---------------------------------------------------------------------------
    //outputs from machine learning can set gaussian filters
    widget.addGaussian(0.75, 1, 0.3, 0, 0);
    widget.setContainer(widgetContainer);
    widget.bindMouseListeners();
    widget.onAnimation((start) => {
        if (start) {
            renderWindow.getInteractor().requestAnimation(widget);
        } else {
            renderWindow.getInteractor().cancelAnimation(widget);
        }
    });
    widget.onOpacityChange(() => {
        widget.applyOpacity(piecewiseFunction);
        if (!renderWindow.getInteractor().isAnimating()) {
            renderWindow.render();
        }
    });
    // ----------------------------------------------------------------------------
    // Expose variable to global namespace
    // ----------------------------------------------------------------------------
    global.widget = widget;
}