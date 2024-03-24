function validateForm() {
   var username = document.forms["login"]["username"].value;
   var password = document.forms["login"]["password"].value;
   var valid = validate(username, password);
   return valid;
}

function validate(username, password) {
   var valid = false;
   var usernameArray = ["JaneDoe"];
   var passwordArray = ["123"];
  
   for (var i = 0; i < usernameArray.length; i++) {
       if (username === usernameArray[i] && password === passwordArray[i]) {
           valid = true;
           break;
       }
   }
   if (valid) {
       // Redirect to Google after successful validation
       window.location.href = "http://www.google.com";
   } else {
       // Perform any other actions if validation fails
       alert("Invalid username or password.");
   }
   return false;
}
module.exports = validate;