
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

// var elem = document.querySelector(".btn_callFileCoin");
// elem.addEventListener('click', function() {
    
//     console.log(this.id)
//     }
//   });

    // const myScript = document.getElementById('bundle');
    // let myArgument = myScript.getAttribute('myargument')
    // console.log(myArgument)


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
// let value = document.querySelectorAll('.btn_callFileCoin').value;
// session_id_callFileCoin
let dataPass = fileCoinData(value);
// this song takes time ## producing code
console.log(dataPass)
// consuming code 

// promise is a special Javascript Object that links the  "producing code" and "consuming code" 

    });
});