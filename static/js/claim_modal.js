// Get the modal
var claimModal = document.getElementById("claimModal");

// Get the button that opens the modal
var claimBtn = document.getElementById("claimBtn");

// Get the <span> element that closes the modal
var span = document.getElementById("closeClaim");

// When the user clicks the button, open the modal 
claimBtn.onclick = function() {
  claimModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  claimModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == claimModal) {
    claimModal.style.display = "none";
  }
}