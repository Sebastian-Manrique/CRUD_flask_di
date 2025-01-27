function agarrarDatos() {
  var passStr = document.getElementById("passAdmin");
  var passFinal = passStr.value;
  var email = document.getElementById("email");
  var emailFinal = email.value;
  console.log("Contraseña: %s, correo: %s" + passFinal, emailFinal);
}

function myFunction() {
  // Para mostrar o no la contraseña
  var x = document.getElementById("passEmpleado");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function myFunction2() {
  document.getElementById("welcomeDiv").style.display = "block";
}