var files = [];
var _dataArray = [];
var _filenames = [];
<script src="assets/js/xtk.js"></script>
$(document).ready(function() {
  $("#file_inp").change(function() {
    files = document.getElementById("file_inp").files;

    // create a new test_renderer
    var r = new X.renderer3D();
    r.bgColor = [0.2, 0.25, 0.4];
    r.init();
    r.camera.position = [0, 300, 0];

    // we create the X.volume container and attach all DICOM files
    var v = new X.volume();

    //v.file = urls;

    var counter = files.length;
    var reader = new FileReader();

    recursiveLoading(0, r, v, reader, counter);

  });
});

function recursiveLoading(idx, r, v, reader, counter) {
  if (counter > 0) {
    reader.onload = function(file) {
      var arrayBuffer = reader.result;
      var byteArray = new Uint8Array(arrayBuffer);
      _filenames[idx] = file.name + ".DCM";
      _dataArray[idx] = arrayBuffer; // _dataArray[idx] = byteArray.buffer; // Alternative!
      //_filenames.push(file.name + ".DCM");
      //_dataArray.push(arrayBuffer);
      counter--;

      recursiveLoading(idx + 1, r, v, reader, counter);
    };
    reader.readAsArrayBuffer(files[idx]);
  } else {
    v.file = _filenames;
    v.filedata = _dataArray;
    // add the volume
    r.add(v);

    // .. and render it
    r.render();

    r.onShowtime = function() {

      // activate volume rendering
      v.volumeRendering = true;
      v.lowerThreshold = 80;
      v.windowLower = 115;
      v.windowHigh = 360;
      v.minColor = [0, 0.06666666666666667, 1];
      v.maxColor = [0.5843137254901961, 1, 0];
      v.opacity = 0.2;

    };

    volume = v;
  }
}

// }
// window.onload = function() {
//   var r = new X.renderer2D();
//   r.orientation = 'Z';
//   r.init();
//   var v = new X.volume();
//   v.file = 'assets/D0001.dcm';
//   r.add(v);
//
//   r.onWindowLevel();
//   r.render();
//   var ele=  document.createElement('canvas');
//   ele.setAttribute('id', 'xtkCanvas');
//   r.onShowtime = function() {
//   };
//   volume = v;
// };
