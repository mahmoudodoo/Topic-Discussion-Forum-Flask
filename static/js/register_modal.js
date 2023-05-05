// Get the modal
var registerModal = document.getElementById("registerModal");

// Get the button that opens the modal
var registerBtn = document.getElementById("registerBtn");

// Get the <span> element that closes the modal
var span = document.getElementById("closeRegister");

// When the user clicks the button, open the modal 
registerBtn.onclick = function() {
    registerModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    registerModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == moregisterModaldal) {
    registerModal.style.display = "none";
  }
}