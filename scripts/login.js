function validateForm() {
   let username = document.forms["login"]["username"].value;
   let password = document.forms["login"]["password"].value;
   let valid = validate(username, password);
   return valid;
}

function validate(username, password) {
   let valid = false;
   let usernameArray = ["JaneDoe"];
   let passwordArray = ["123"];
  
   for (var i = 0; i < usernameArray.length; i++) {
       if (username === usernameArray[i] && password === passwordArray[i]) {
           valid = true;
           break;
       }
   }
   if (valid) {
       // Redirect to Google after successful validation
       window.location.href = "../library.html";
   } else {
       // Perform any other actions if validation fails
       alert("Invalid username or password.");
   }
   return false;
}