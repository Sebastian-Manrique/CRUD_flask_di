function mostrarContra() {
  // Para mostrar o no la contraseña, accion directa
  // es el boton, es para registrar, no para login
  var contra = document.getElementById("passCrear");
  var confirmarContra = document.getElementById("passCrearConfirmar");

  if (contra.type === "password") {
    contra.type = "text";
    confirmarContra.type = "text";
  } else {
    contra.type = "password";
    confirmarContra.type = "password";
  }
}

function cambiarCuenta() {
  /*Funcion para el onclick del switch para cambiar el texto*/
  var usuario = document.getElementById("seleccionCuenta");
  usuario.innerHTML = usuario.innerHTML == "Usuario" ? "Admin" : "Usuario";
}

function botonMostrarContra() {
  // Para mostrar o no la contraseña
  document.getElementById("divBotonMostrar").style.display = "block";
}

function crearUsuario() {
  var usuario = document.getElementById("usuarioCrear");
  var contra = document.getElementById("passCrear");
  var confirmarContra = document.getElementById("passCrearConfirmar");
  var email = document.getElementById("emailCrear");
  var usuarioTipo = document.getElementById("seleccionCuenta").innerHTML;

  if (
    contra.value == "" ||
    confirmarContra.value == "" ||
    email.value == "" ||
    usuario.value == ""
  ) {
    alert("Por favor, llena todos los campos");
    return;
  }

  if (contra.value != confirmarContra.value) {
    alert("Las contraseñas no coinciden");
    return;
  }

  // console.log(
  //   //  debug
  //   "Usuario: " +
  //     usuario.value +
  //     "\ncorreo: " +
  //     email.value +
  //     "\nContraseña: " +
  //     contra.value +
  //     "\nTipo de usuario: " +
  //     usuarioTipo
  // );
  callCreate(usuario.value, contra.value, email.value, usuarioTipo);
}

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

async function callCreate(usuario, contra, email, tipo) {
  try {
    const response = await fetch(
      `/api/crearCuenta?_usuario=${usuario}&_contra=${contra}&_email=${email}&_tipo=${tipo}`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    //DEBUG
    // console.log(data);

    // Para mostrar o no el gif
    document.getElementById("cargando").style.display = "block";
    document.getElementById("botonEnviar").hidden = true;

    // Esperar 1 segundos antes de redirigir
    await delay(1000);

    window.location.replace("/hecho");
  } catch (error) {
    console.error("Error:", error);
  }
}
