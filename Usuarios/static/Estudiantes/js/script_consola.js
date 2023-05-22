$(document).ready(function() {
  var isOpen = false;

  $('#userDropdown').on('click', function() {
    if (isOpen) {
      $('.dropdown-menu').removeClass('show');
      isOpen = false;
    } else {
      $('.dropdown-menu').addClass('show');
      isOpen = true;
    }
  });

  $(document).on('click', function(e) {
    var target = $(e.target);
    if (!target.is('#userDropdown') && !target.closest('.dropdown-menu').length) {
      $('.dropdown-menu').removeClass('show');
      isOpen = false;
    }
  });
});


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