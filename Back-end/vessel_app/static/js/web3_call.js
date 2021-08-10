
// import { Web3Storage } from 'web3.storage'
import { Web3Storage } from 'web3.storage/dist/bundle.esm.min.js'
// import { dataSend } from 'web3.storage/dist/bundle.esm.min.js'
export function test(data) {
    console.log(data);
};

function getAccessToken() { 
    // push API key only for testing purposings
    return ''
  }
function makeStorageClient() {
    return new Web3Storage({ token: getAccessToken() })
}
//File Constructor
function makeFileObjects(medical_data) {
    const obj = { hello: medical_data }
    const blob = new Blob([JSON.stringify(obj)], {type : 'application/json'})
  
    const files = [
      new File(['contents-of-file-1'], 'plain-utf8.txt'),
      new File([blob], 'test.json')
    ]
    // nott saving test.json file for some reason
    return files

  }

 //we need array of files 
 async function uploadDatatoFileCoin(files) {
    const client = makeStorageClient()
    const cid = await client.put(files)
    console.log('stored files with cid:', cid)
    return cid
  
}

export function fileCoinStore(data) { 
    console.log("Hello FileCoinStore")
    makeStorageClient()
    const files = makeFileObjects(data)
    const cid = uploadDatatoFileCoin(files)
    console.log("did we recevie cid?", cid)

    // when uploading files put request are bundled into one content achive CAR
    return cid
}


// {{url_for('file_pipeline.fileCoinCall')}}
function fileCoinData(value) {
    // we need to pass the value or session idea in the post
    var xml = new XMLHttpRequest();
    var session_id = value
    xml.open("POST","http://127.0.0.1:5000/fileCoinCall", true)
    xml.setRequestHeader("Content-type","application/x-www-form-urlencoded");
      // recevice information after request
    xml.onload = function(){
    var dataReply = JSON.parse(this.responseText);
    console.log("we have data?", dataReply)
    // mainCall(dataReply)
    return dataReply
    };  

    var dataSend = JSON.stringify({
    'session_id':session_id
    });

    xml.send(dataSend);
    //end function
}



function cidToBackend(value){
  var xml = new XMLHttpRequest();
  var cid = value

  xml.open("POST","http://127.0.0.1:5000/storeCID", true)
  xml.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  
  // what does onload do?
  xml.onload = function(){
    var dataReply = JSON.parse(this.responseText);
    console.log('sucess', dataReply)
    return 'success'
    };  

  var dataSend = JSON.stringify({
    'cid':cid
    });

    xml.send(dataSend);


}
// https://www.pluralsight.com/guides/handling-nested-promises-using-asyncawait-in-react
// we want out async function to call Web3Storage then wait for return CID 
// then POST CID to backend
async function StoreDataIntoFileCoin(value) {
  try { 
  var dataReply = await fileCoinData(value)
  console.log("try 1st async call", dataReply) // these return undefined?
  }
  catch (error) { 
    console.log("error" + error)  // these return undefined?
  }
  finally{ 
    console.log("finally async call", dataReply)  // these return undefined?
  }
  // console.log("async pass from fileCoinData", Data.cid)
  const cid = await fileCoinStore(dataReply)
  // immediately one after another.
  const status = await cidToBackend(cid)
  return status
}

// async function cidToBackendCall(cid){
//   const cidReturn = await cidToBackend(cid)
//   console.log("async call from backend?", cidReturn.cid)
//   return cidReturn.cid
// }

// microtask???


// https://stackoverflow.com/questions/52180443/javascript-change-only-one-button-by-click-with-id-and-addeventlistener
// getElementbyId is only for one element so second button doesnt work 
// document.getElementById("buttonPress").addEventListener("click", function() {
document.querySelectorAll('.btn_callFileCoin').forEach(function(btn){
        btn.addEventListener('click', function() {
            console.log(this.id)
            // var inputs = $(".session_id_callFileCoin");
            // for(var i = 0; i < inputs.length; i++){
            //     console.log($(inputs[i]).val());
            // }
let value = this.id

console.log("before", value)
const storeFS = StoreDataIntoFileCoin(value)
console.log(storeFS)

// this needs to be contained in promised 
// let dataPass, cid = fileCoinData(value);
// // this song takes time ## producing code
// console.log("CID returned", cid)
// console.log("data return after call", dataPass)

// promise is a special Javascript Object that links the  "producing code" and "consuming code" 

    });
});