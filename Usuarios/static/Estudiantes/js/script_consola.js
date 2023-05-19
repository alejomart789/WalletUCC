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

function mostrarCampoAbono() {
  var campoAbono = document.getElementById('campo-abono');
  campoAbono.style.display = event.target.checked ? 'block' : 'none';
}