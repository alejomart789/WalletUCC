/* Código JavaScript para la página */

function cambiarTexto() {
    var boton = document.getElementById("boton-header");
    boton.innerHTML = "Registrarte";
}

function restaurarTexto() {
    var boton = document.getElementById("boton-header");
    boton.innerHTML = "Iniciar Sesión";
  }
  

/* Función que se ejecuta cuando se carga la página */
$(document).ready(function() {
    console.log("La página ha cargado.");
    
    // Asignar la función al evento onmouseover del botón
    $('#boton-header').on('mouseover', cambiarTexto);
    $('#boton-header').on('mouseout', restaurarTexto);
});

