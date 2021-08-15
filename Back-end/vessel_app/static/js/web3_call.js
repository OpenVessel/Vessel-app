// import { Web3Storage } from 'web3.storage'
import { Web3Storage } from 'web3.storage/dist/bundle.esm.min.js'

// Citation
// https://stackoverflow.com/questions/52180443/javascript-change-only-one-button-by-click-with-id-and-addeventlistener
// https://www.pluralsight.com/guides/handling-nested-promises-using-asyncawait-in-react
export function test(data) {
    console.log(data);
};

function getAccessToken() { 
    // push API key only for testing purposings
    return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDE3QTM5MDQ5ZmZBMTk1MDExMGFDOGNhQ0MyQ0YyNmFmNmJjMEUwOWUiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2MjgwMDIzMzkyOTgsIm5hbWUiOiJPcGVuVmVzc2VsIn0.eY7q_BaPj0EuV6dQC2zCD-BEhcHwR741wj1eijwaKS8'
  }
function makeStorageClient() {
    return new Web3Storage({ token: getAccessToken() })
}

function retrieveDatatoFileCoin(cid){
  const client = makeStorageClient()
  const res = client.get(cid)
  // console.log('Response from FileCoin[${res.status}] ${res.statusText}')
  // if (!res.ok) {
  //   throw new Error(`failed to get ${cid} - [${res.status}] ${res.statusText}`)
  // }

  return res
}


 //we need array of files 
function uploadDatatoFileCoin(files) {
    const client = makeStorageClient()
    const cid = client.put(files)
    console.log('stored files with cid:', cid)
    return cid
  
}

function fileCoinStore(medical_data, value){
  return new Promise(function(resolve, reject){
    // const obj = { hello: medical_data }
    // const blob = new Blob([JSON.stringify(obj)], {type : 'application/json'})
    const blob = new Blob([JSON.stringify(medical_data)], {type : 'application/json'})
    const files = [
      new File([blob], value + '_test.json')
    ]
  
  resolve(files)

    

  });
}

function fileCoinData(value) {
  return new Promise(function(resolve, reject) {
    let xhr = new XMLHttpRequest();
    let session_id = value

    xhr.open("POST","http://127.0.0.1:5000/fileCoinCall", true)

    xhr.onload = function () {
      if (this.status >= 200 && this.status < 300) {
        var dataReply = JSON.parse(this.responseText);  
        resolve(dataReply);
      } else {
          reject({
              status: this.status,
              statusText: xhr.statusText
          });
      }
    };
    xhr.onerror = function () {
      reject({
          status: this.status,
          statusText: xhr.statusText
      });
  };
  var dataSend = JSON.stringify({
    'session_id':session_id
    });

  xhr.send(dataSend);

  });
}
function cidToBackend(cid_pass, value) {
  return new Promise(function(resolve, reject) {
    let xhr = new XMLHttpRequest();
    var cid = cid_pass
    let session_id = value
    

    xhr.open("POST","http://127.0.0.1:5000/storeCID", true)
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");

    xhr.onload = function () {
      if (this.status >= 200 && this.status < 300) {
        var dataReply = JSON.parse(this.responseText);  
        resolve(dataReply);
      } else {
          reject({
              status: this.status,
              statusText: xhr.statusText
          });
      }
    };
    xhr.onerror = function () {
      reject({
          status: this.status,
          statusText: xhr.statusText
      });
  };
  var dataSend = JSON.stringify({
    'cid':cid,
    'session_id':session_id
    });

  xhr.send(dataSend);

  });
}

function postDatatoBackend(data_pass, cid_pass) {
  return new Promise(function(resolve, reject) {
    let xhr = new XMLHttpRequest();
    var data = data_pass
    var cid = cid_pass
    
    

    xhr.open("POST","http://127.0.0.1:5000/restoreDataObjectCID", true)
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");

    xhr.onload = function () {
      if (this.status >= 200 && this.status < 300) {
        var dataReply = JSON.parse(this.responseText);  
        resolve(dataReply);
      } else {
          reject({
              status: this.status,
              statusText: xhr.statusText
          });
      }
    };
    xhr.onerror = function () {
      reject({
          status: this.status,
          statusText: xhr.statusText
      });
  };
  var dataSend = JSON.stringify({
    'cid':cid,
    'data':data
    });

  xhr.send(dataSend);

  });
}


// Async function called from here
async function StoreDataIntoFileCoin(value) {

  var dataReply = await fileCoinData(value) // async now works
  var files = await fileCoinStore(dataReply, value) //async now works 
  var cid = await uploadDatatoFileCoin(files)
  console.log("did we recevie cid?", cid)

  var status = await cidToBackend(cid, value)

  return status
}

async function RetrieveDataFromFileCoin(cid) {
  var resp = await retrieveDatatoFileCoin(cid)
  console.log(resp)
  const files = await resp.files()
  console.log(files)
  let read = new FileReader();
  for (const file of files){

    read.readAsBinaryString(file);
    let data_pass = read.result
    read.onloadend = function(){
    console.log(read.result)
    postDatatoBackend(read.result, cid)
    }
  }

}
// microtask???
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
let value = this.id
const retFS = RetrieveDataFromFileCoin(value)
console.log(retFS)
// HTTP gateway
// Web3.Storage JavaScript client 



});
});
