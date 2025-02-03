document
  .getElementById("botonCrearJuego")
  .addEventListener("click", async function () {
    const { value: formValues } = await Swal.fire({
      // Gracias por existir - Eros Ramazzi 🙌🙌🙌
      title: "Ingrese los datos del juego",
      html:
        '<input id="swal-input1" class="swal2-input" placeholder="Nombre">' +
        '<input id="swal-input2" class="swal2-input" placeholder="Precio">' +
        '<input id="swal-input3" class="swal2-input" placeholder="Descripción">',
      focusConfirm: false,
      preConfirm: () => {
        return [
          document.getElementById("swal-input1").value,
          document.getElementById("swal-input2").value,
          document.getElementById("swal-input3").value,
        ];
      },
    });

    if (formValues) {
      Swal.fire({
        title: "Datos recibidos",
        html: `Nombre: ${formValues[0]}<br>Precio: ${formValues[1]} € <br>Descripción: ${formValues[2]}`,
        icon: "success",
      });

      try {
        var usuarioId = document.getElementById("usuarioId").textContent;

        const response = await fetch(
          `/api/crearJuego?_nombre=${formValues[0]}&_precio=${formValues[1]}&_dscrp=${formValues[2]}&_userId=${usuarioId}`
        );

        const data = await response.json();

        //DEBUG
        console.log(data);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
  });

function mostrarContra() {
  //Boton para ver la contraseña del usuario, pero para el apartado del usuario
  let passElement = document.getElementById("mostrarContra");
  passElement.classList.toggle("blurred");
}
