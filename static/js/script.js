function agarrarDatos(str) {
  var contra = "";
  var email = "";
  if (str == "admin") {
    var passStr = document.getElementById("passAdmin");
    contra = passStr.value;
    var emailStr = document.getElementById("email");
    email = emailStr.value;
    // console.log("Contraseña admin: " + contra + " correo: " + email);
  } else if (str == "empleado") {
    var passStr = document.getElementById("passEmpleado");
    contra = passStr.value;
    var emailStr = document.getElementById("emailEmpleado");
    email = emailStr.value;
    // console.log("Contraseña empleado: " + contra + " correo: " + email);
  } else if (contra == "" || email == "") {
    alert("Por favor, llena todos los campos");
    return;
  }
  callAPI(contra, email);
}

async function callAPI(contra, email) {
  const response = await fetch(
    `http://127.0.0.1:5000/api/agarrarDatos?_contra=${contra}&_email=${email}`
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      // console.log(data);
    });
}

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
