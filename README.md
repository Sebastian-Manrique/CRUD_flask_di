# CRUD de Sebastian Manrique

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=git,python,flask,javascript,html,css" />
  </a>
</p>

ES: Descripción: Una página web que muestra estadísticas y detalles de equipos y jugadores de fútbol. Los datos se obtienen de una API de fútbol en tiempo real.

EN: Description: A website that displays statistics and details of football teams and players. The data is obtained from a real-time football API.

# Descripción del Proyecto
Este proyecto requiere ciertas dependencias que están listadas en el archivo `requirements.txt`. Puedes instalar todas las dependencias necesarias utilizando conda.

## Requisitos
- **Conda**: Asegúrate de tener conda instalado en tu sistema. Puedes descargar e instalar conda desde [Anaconda](https://www.anaconda.com/) o [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

## Instalación
Para instalar las dependencias del proyecto, sigue estos pasos:

1. **Crear un entorno conda** (si no tienes uno ya creado):

    ```sh
    conda create --name myenv python=3.11
    ```
    Reemplaza `myenv` con el nombre que desees para tu entorno y `3.11` con la versión de Python que prefieras.

2. **Activar el entorno conda**:

    ```sh
    conda activate myenv
    ```

3. **Instalar las dependencias desde `requirements.txt`**:

    ```sh
    conda install --name myenv --file requirements.txt
    ```
    Asegúrate de estar en el directorio donde se encuentra `requirements.txt` o proporciona la ruta completa al archivo.
