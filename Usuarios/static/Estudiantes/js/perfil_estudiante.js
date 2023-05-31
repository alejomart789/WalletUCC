$(document).ready(function() {
    // Mostrar el nombre del archivo seleccionado en el input file
    $('#profile-pic-input').change(function() {
      var fileName = $(this).val().split('\\').pop();
      $(this).next('.custom-file-label').html(fileName);
      
      // Mostrar una vista previa de la imagen
      var file = this.files[0];
      if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
          $('#profile-pic-preview').attr('src', e.target.result);
        }
        reader.readAsDataURL(file);
      } else {
        $('#profile-pic-preview').attr('src', '');
      }
    });
});