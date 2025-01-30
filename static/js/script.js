function mostrarContra(str) {
  // Para mostrar o no la contraseña, accion directa
  // ES EL BOTON
  var x = "";
  if (str == "admin") {
    x = document.getElementById("passAdmin");
  } else {
    x = document.getElementById("passEmpleado");
  }
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function botonMostrarContra(str) {
  // Para mostrar o no la contraseña
  if (str == "admin") {
    document.getElementById("divBotonMostrarAdmin").style.display = "block";
  } else {
    document.getElementById("divBotonMostrarEmpleado").style.display = "block";
  }
}
