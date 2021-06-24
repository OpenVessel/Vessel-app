
console.log('Hello world');  
// comment igonred by engine 
// Explain why and how 
// spreate concerns 
// html is content
// js is behavior 

const interestRate = 0.3;
// interestRate = 1;
console.log(interestRate)

let name = 'Mosh'; // String 
let age = 30; // Number
let isApproved = false; // Boolean
let setColored = null; // null
let person = {
    name:'Mosh',
    age:30

}; 

console.log(person)
// dot notation
person.age =31;
console.log(person)

// Bracket Notation 
person['name'] = 'Leslie';
let selection = 'name';
person[selection] = 'Mary';

console.log(person)
//https://material-ui.com/
// Array literl 
let selectedColors = ['red', 'blue'];
selectedColors[2] = 'green';
console.log(selectedColors[2]);

// functions 
function greet(name) { 
//func has one parameter
    console.log('Hello World' + name);

}
name = 'leslie';
//calling func
//argurement passed into the functions
greet(name);



// Statically typed language
// Dynamically-typed the type of variable can change at run time

console.log(typeof(name))
//


//typeof() will return the type of value in its parameters.
//some examples of types: undefined, NaN, number, string, object, array
value = 'test'
//example of a practical usage
if (typeof(value) !== "undefined") {//also, make sure that the type name is a string
    //execute code
    console.log(value)
}

// REFERENCE TYPES
// Object array
// Functions



// exports.is = (data) => {
//     const isArray = Array.isArray(data) && 'array'
//     const isObject = data == {} && 'object'
//     const isNull =  data == null && 'null'
    
//     const isGrouping =  isArray || isObject || isNull
//     const isCheck = !isGrouping ? typeof data : isGrouping
    
//     const isTypeData = ['number','string','array','symbol','object','undefined','null','function', 'boolean']
//     const isMatch = isTypeData.indexOf(isCheck)
//     const isResult = isTypeData[isMatch]
//     return isResult
//     }

// combinded javascript files into a bundle and serve to the client
// Nodei is a runtime enviroment to execute Javascript code
// variables stores data into memory variable is like a box