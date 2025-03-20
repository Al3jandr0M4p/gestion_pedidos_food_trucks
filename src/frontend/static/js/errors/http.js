const params = new URLSearchParams(window.location.search);
const code = params.get("code") || "Unknow";
const message = params.get("message") || "Ocurrio un error inesperado.";

document.getElementById("error-code").textContent `Error ${code}`;
document.getElementById('error-message').textContent = message;