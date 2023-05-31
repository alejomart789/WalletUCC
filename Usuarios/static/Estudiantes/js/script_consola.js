// Agrega un evento click al enlace del nombre de perfil
document.getElementById("profileName").addEventListener("click", toggleDropdown);

// Agrega un evento click a la imagen de perfil
document.getElementById("profileImage").addEventListener("click", toggleDropdown);

// Agrega un evento click al enlace de notificaciones
document.getElementById("alertsDropdownLink").addEventListener("click", toggleDropdown2);

// Agrega un evento click al enlace del centro de mensajes
document.getElementById("messagesDropdownLink").addEventListener("click", toggleDropdown3);

// Función para alternar la visualización del menú desplegable
function toggleDropdown() {
    var dropdownMenu = document.getElementById("userDropdown");
    dropdownMenu.classList.toggle("show");

    // Cierra el menú desplegable si se hace clic fuera de él
    window.addEventListener("click", function (event) {
        if (!dropdownMenu.contains(event.target) && !event.target.matches("#profileName, #profileImage")) {
            dropdownMenu.classList.remove("show");
        }
    });
}

// Función para alternar la visualización del menú desplegable de notificaciones
function toggleDropdown2(event) {
    event.stopPropagation(); // Detiene la propagación del evento click para evitar cerrar el menú inmediatamente

    var dropdownMenu = document.getElementById("alertsDropdown").querySelector(".dropdown-menu");
    dropdownMenu.classList.toggle("show");

    // Cierra el menú desplegable si se hace clic fuera de él
    window.addEventListener("click", function (event) {
        if (!dropdownMenu.contains(event.target) && !event.target.matches("#alertsDropdownLink")) {
            dropdownMenu.classList.remove("show");
        }
    });
}

// Función para alternar la visualización del menú desplegable del centro de mensajes
function toggleDropdown3(event) {
    event.stopPropagation(); // Detiene la propagación del evento click para evitar cerrar el menú inmediatamente

    var dropdownMenu = document.getElementById("messagesDropdown").querySelector(".dropdown-menu");
    dropdownMenu.classList.toggle("show");

    // Cierra el menú desplegable si se hace clic fuera de él
    window.addEventListener("click", function (event) {
        if (!dropdownMenu.contains(event.target) && !event.target.matches("#messagesDropdownLink")) {
            dropdownMenu.classList.remove("show");
        }
    });
}





function abrirPopup() {
  var popup = document.getElementById("popup");
  var overlay = document.getElementById("popup-overlay");
  popup.style.display = "block";
  overlay.style.display = "block";
}

function cerrarPopup() {
  var popup = document.getElementById("popup");
  var overlay = document.getElementById("popup-overlay");
  popup.style.display = "none";
  overlay.style.display = "none";
}

function mostrarCampoAbono() {
  var campoAbono = document.getElementById('campo-abono');
  campoAbono.style.display = event.target.checked ? 'block' : 'none';
}