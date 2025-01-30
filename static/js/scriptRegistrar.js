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

function botonMostrarContra() {
  // Para mostrar o no la contraseña
  document.getElementById("divBotonMostrar").style.display = "block";
}

function crearUsuario() {
  var usuario = document.getElementById("usuarioCrear");
  var contra = document.getElementById("passCrear");
  var confirmarContra = document.getElementById("passCrearConfirmar");
  var email = document.getElementById("emailCrear");

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

  //   console.log(
  //     //  debug
  //     "Usuario: " +
  //       usuario.value +
  //       "\ncorreo: " +
  //       email.value +
  //       "\nContraseña: " +
  //       contra.value
  //   );
  callCreate(usuario.value, contra.value, email.value);
}

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

async function callCreate(usuario, contra, email) {
  try {
    const response = await fetch(
      `/api/crearCuenta?_usuario=${usuario}&_contra=${contra}&_email=${email}`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log(data);

    // Esperar 1 segundos antes de redirigir
    await delay(1000);

    window.location.replace("/hecho");
  } catch (error) {
    console.error("Error:", error);
  }
}
