
// import { Web3Storage } from 'web3.storage'
import { Web3Storage } from 'web3.storage/dist/bundle.esm.min.js'
// import { dataSend } from 'web3.storage/dist/bundle.esm.min.js'
export function test(data) {
    console.log(data);
};


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
    console.log(dataReply)
    // mainCall(dataReply)
    test(dataReply)
    let dataPass = dataReply
    return dataPass
    };  
    var dataSend = JSON.stringify({
    'session_id':session_id
    });

    xml.send(dataSend);
    //end function
}
// https://stackoverflow.com/questions/52180443/javascript-change-only-one-button-by-click-with-id-and-addeventlistener
// getElementbyId is only for one element so second button doesnt work 
// document.getElementById("buttonPress").addEventListener("click", function() {
document.querySelectorAll('.btn_callFileCoin').forEach(function(btn){
        btn.addEventListener('click', function() {
      
    // same bug
let value = document.getElementById('session_id').value;
// let value = document.querySelectorAll('.btn_callFileCoin').value;
// session_id_callFileCoin
let promise = new Promise(function(resolve, reject) {
    // executor (the producing code, "singer")
    let dataR = fileCoinData(value);
  });

promise.then( 
        console.log(result)
    )
console.log(dataR)
// this song takes time ## producing code

// consuming code 

// promise is a special Javascript Object that links the  "producing code" and "consuming code" 



    });
});