$(document).ready(function() {
    var timeout;
    $('.nav-item.dropdown').on('mouseenter', function() {
      clearTimeout(timeout);
      $(this).find('.dropdown-menu').addClass('show');
    }).on('mouseleave', function() {
      var $self=$(this);
      timeout = setTimeout(function(){
          $self.find('.dropdown-menu').removeClass('show');
      }, 500);
    });

    $('#userDropdown').on('mouseleave', function() {
      timeout = setTimeout(function(){
          $('.dropdown-menu').removeClass('show');
      }, 500);
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

function obtenerOpcionSeleccionada() {
  var opcionSeleccionada = document.querySelector('input[name="opcion"]:checked').value;

  if (opcionSeleccionada === "pago_total") {
    var valor = 1000; // Valor del pago total (ejemplo)
    alert("Pago total: $" + valor);
  } else if (opcionSeleccionada === "abono") {
    var valorAbono = document.getElementById("valor-abono").value;
    alert("Abono: $" + valorAbono);
  }

  cerrarPopup();
}

function mostrarCampoAbono() {
  var opcionAbono = document.querySelector('input[value="abono"]');
  var campoAbono = document.getElementById("campo-abono");

  if (opcionAbono.checked) {
    campoAbono.style.display = "block";
  } else {
    campoAbono.style.display = "none";
  }
}