//#################### Script creado por Sebastian Manrique ####################

//variable para recargar la tabla
const delay = (ms) => new Promise((res) => setTimeout(res, ms));

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
      showCancelButton: true,
      cancelButtonColor: "#c31313",
      cancelButtonText: "Cancelar",
      confirmButtonText: "Crear juego",
      confirmButtonColor: "#4cb052",
      preConfirm: () => {
        return [
          document.getElementById("swal-input1").value,
          document.getElementById("swal-input2").value,
          document.getElementById("swal-input3").value,
        ];
      },
    });

    precio = "" + formValues[1];
    if (formValues) {
      if (precio.includes(",")) {
        alert("El precio contiene una coma");
        return false; // Evita que el se cierre
      }
      Swal.fire({
        title: "Datos recibidos",
        html: `Nombre: ${formValues[0]}<br>Precio: ${formValues[1]} € <br>Descripción: ${formValues[2]}`,
        icon: "success",
        confirmButtonColor: "#4caf50",
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
  let boton = document.getElementById("botonMostrarContra");
  let passElement = document.getElementById("mostrarContra");
  passElement.classList.toggle("blurred");
  boton.textContent =
    boton.textContent === "Ocultar" ? "Mostrar contraseña" : "Ocultar";
}

// Selecciona todos los botones con la clase "botonModificar" para modificar un juego
document.querySelectorAll(".botonModificar").forEach((boton) => {
  boton.addEventListener("click", async function () {
    // Encuentra la fila en la que se hizo clic
    let fila = this.closest("tr");
    let celdas = fila.cells;

    // Extrae los valores de las celdas
    let idJuego = celdas[0].innerText;
    let nombreJuego = celdas[1].innerText;
    let precioJuego = celdas[2].innerText;
    let descripcionJuego = celdas[3].innerText;

    // Muestra el formulario con los datos actuales del juego
    const { value: formValues } = await Swal.fire({
      title: "Modificar juego",
      html: `
        <input id="swal-input1" class="swal2-input" value="${nombreJuego}" placeholder="Nombre del juego">
        <input id="swal-input2" class="swal2-input" value="${precioJuego}" placeholder="Precio">
        <input id="swal-input3" class="swal2-input" value="${descripcionJuego}" placeholder="Descripción">
      `,
      focusConfirm: false,
      showCancelButton: true,
      cancelButtonColor: "#c31313",
      cancelButtonText: "Cancelar",
      confirmButtonText: "Guardar cambios",
      confirmButtonColor: "#4cb052",
      preConfirm: () => {
        precio = "" + document.getElementById("swal-input2").value;
        if (precio.includes(",")) {
          alert("El precio contiene una coma");
          return false; // Evita que el se cierre
        } else {
          return {
            id: idJuego,
            nombre: document.getElementById("swal-input1").value,
            precio: document.getElementById("swal-input2").value,
            descripcion: document.getElementById("swal-input3").value,
          };
        }
      },
    });

    // Si el usuario presionó "Guardar cambios", procesa los datos
    if (formValues) {
      try {
        //Fetch a la API para modificar el juego
        const response = await fetch(
          `/api/modificarJuego?_id=${formValues.id}&_nombre=${formValues.nombre}&_precio=${formValues.precio}&_dscrp=${formValues.descripcion}`
        );

        const data = await response.json();

        //DEBUG
        // console.log(data);
        console.log("Recargando . . . .");
        recargarTabla;
        console.log("Recargado!");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
  });
});

document.querySelectorAll(".botonEliminar").forEach((boton) => {
  //Funcion para eliminar un juego de la BDD
  boton.addEventListener("click", async function () {
    Swal.fire({
      title: "¿Estás seguro?",
      text: "Esta acción no se puede deshacer.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#4caf50",
      cancelButtonColor: "#ff0000",
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Cancelar",
    }).then(async (result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "¡Eliminado!",
          text: "El juego ha sido eliminado.",
          confirmButtonColor: "#4caf50",
        });

        // Encuentra la fila en la que se hizo clic
        let fila = this.closest("tr");
        let celdas = fila.cells;

        // Extrae el id de la celda
        let idJuego = celdas[0].innerText;

        try {
          //Fetch a la API para modificar el juego
          const response = await fetch(`/api/eliminarJuego?_id=${idJuego}`);
          //DEBUG
          // console.log(data);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
        } catch (error) {
          console.error("Error:", error);
        }
      }
    });
    recargarTabla;
  });
});

function recargarTabla() {
  console.log("dentro de recargar tabla");
  // fetch("/get_juegos") // Hacemos la solicitud a la ruta que devuelve los juegos
  //   .then((response) => response.json()) // Convertimos la respuesta a JSON
  //   .then((juegos) => {
  //     // Seleccionamos el tbody donde vamos a actualizar los datos
  //     const tbody = document.querySelector("#miTabla tbody");
  //     tbody.innerHTML = ""; // Limpiamos la tabla

  //     // Iteramos sobre los juegos y creamos las filas de la tabla
  //     juegos.forEach((juego) => {
  //       const row = document.createElement("tr");

  //       // Creamos cada celda de la fila
  //       row.innerHTML = `
  //                 <td>${juego.id}</td>
  //                 <td>${juego.nombre}</td>
  //                 <td>${juego.precio}</td>
  //                 <td>${juego.descripcion}</td>
  //                 <td>${juego.usuario_id}</td>
  //                 <td><button class="botonModificar">Modificar juego</button></td>
  //                 <td><button class="botonEliminar">Eliminar juego</button></td>
  //             `;

  //       // Añadimos la fila al tbody
  //       tbody.appendChild(row);

  //       console.log("Juego ID: " + juego.id);
  //       console.log("Nombre: " + juego.nombre);
  //       console.log("Precio: " + juego.precio);
  //       console.log("Descripción: " + juego.descripcion);
  //       console.log("ID Usuario: " + juego.usuario_id);
  //     });
  //   })
  //   .catch((error) => console.error("Error al cargar los juegos:", error));

  fetch("/get_juegos")
    .then((response) => response.json())
    .then((data) => console.log(data))
    .catch((error) => console.error("Error en la API:", error));
}
