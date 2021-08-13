
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

async function retrieveDatatoFileCoin(cid){
  const client = makeStorageClient()
  const res = await client.get(cid)
  console.log('Response from FileCoin[${res.status}] ${res.statusText}')
  if (!res.ok) {
    throw new Error(`failed to get ${cid} - [${res.status}] ${res.statusText}`)
  }

  const files = await res.files()
  for (const file of files) {
    console.log(`${file.cid} -- ${file.path} -- ${file.size}`)
  }


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



function cidToBackend(cid, value){
  var xml = new XMLHttpRequest();
  var cid = cid
  var session_id = value

  xml.open("POST","http://127.0.0.1:5000/storeCID", true)
  xml.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  
  // what does onload do?
  xml.onload = function(){
    var dataReply = JSON.parse(this.responseText);
    console.log('sucess', dataReply)
    return 'success'
    };  

  var dataSend = JSON.stringify({
    'cid':cid,
    'session_id':session_id
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
  const status = await cidToBackend(cid, value)

  return status
}

async function RetrieveDataFromFileCoin(cid) {
  var resp = await retrieveDatatoFileCoin(cid)


}


// microtask???
// https://stackoverflow.com/questions/52180443/javascript-change-only-one-button-by-click-with-id-and-addeventlistener
// store data on FileCoin
document.querySelectorAll('.btn_callFileCoin').forEach(function(btn){
        btn.addEventListener('click', function() {
console.log(this.id)
let value = this.id
console.log("before", value)
const storeFS = StoreDataIntoFileCoin(value)
console.log(storeFS)

    });
});

// reterive data from file coin
document.querySelectorAll('.btn_RetFileCoin').forEach(function(btn){
  btn.addEventListener('click', function() {
console.log(this.id)
// all the data stored with Web3 goes via IPFS conttent-addressed data

// HTTP gateway
// Web3.Storage JavaScript client 



});
});
