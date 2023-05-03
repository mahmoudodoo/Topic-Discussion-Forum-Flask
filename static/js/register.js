function verifyPassword() {  
    var pw = document.getElementById("password").value;
    var cpw = document.getElementById("confirmpassword").value;
    if (pw !== cpw){
        document.getElementById("message").innerHTML = "**Passwords not Match!";
        console.log("password= "+pw+"\n")
        console.log("confirm password= "+cpw+"\n")
    }
    else{
        document.getElementById("message").innerHTML = "";
        console.log("password= "+pw+"\n")
        console.log("confirm password= "+cpw+"\n")
    }
}