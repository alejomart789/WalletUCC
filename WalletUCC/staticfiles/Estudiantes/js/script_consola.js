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
  