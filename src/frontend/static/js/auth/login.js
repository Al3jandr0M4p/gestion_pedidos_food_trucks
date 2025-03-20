document.getElementById("togglePassword").addEventListener("click", function() {
    let passwdInput = document.getElementById("passwd");
    if (passwdInput.type === "password") {
        passwdInput.type = "text";
        this.textContent = "🙈";
    } else {
        passwdInput.type = "password";
        this.textContent = "👁️";
    }
});