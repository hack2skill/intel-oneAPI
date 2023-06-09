// const firebaseConfig = {
//   apiKey: "AIzaSyDTlccqFSlWY5PG2B9o_HF3gXpfjoUADmk",
//   authDomain: "feedback-5e444.firebaseapp.com",
//   databaseURL: "https://feedback-5e444-default-rtdb.firebaseio.com",
//   projectId: "feedback-5e444",
//   storageBucket: "feedback-5e444.appspot.com",
//   messagingSenderId: "902161889127",
//   appId: "1:902161889127:web:1b2077d3c9cc421018a1c2",
// };

// //Initialize database
// firebase.initializeApp(firebaseConfig);

// //reference your database
// var feedback = firebase.database().ref("feedback");

// document.getElementById("feedback").addEventListener("submit", submitForm);

// function submitForm(e) {
//   e.preventDefault();

//   var email = getElementVal("email");
//   var message = getElementVal("message");

//   console.log(email, message);
// };

// // const saveMessage = (email,message) => {
// //     var newfeedback = feedback.push();

// //     newfeedback.set({
// //         email:email,
// //         message:message,
// //     })
// // };

// const getElementVal = (id) => {
//   return document.getElementById(id).value;
// };


