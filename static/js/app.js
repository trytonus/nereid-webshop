// Script to hide Special offers ticker when you click on close icon
$('.new-offers .fa-times-circle').click(function() {
  event.preventDefault();
   $('.new-offers').hide();
});

// Script which keeps the menu bar on the top when the site scrolls down.
$(function(){
  if ($('.sticky').length == 0) {
    return;
  }
  var stickyTop = $('.sticky').offset().top; // returns number
  $(window).scroll(function(){ // scroll event
    var windowTop = $(window).scrollTop(); // returns number
    if (stickyTop < windowTop) {
      $('.sticky').css({ position: 'fixed', top: 0 });
    } else {
      $('.sticky').css('position','static');
    }
  });
});

$(function() {

  $(document).on('click', '.view-switch .grid-view', function(event) {
    event.preventDefault();
    $('.product-description').hide();

    var list = $(".list-view");
    var grid = $(".grid-view");

    if ( list.hasClass('select')) {
      $(".product-list-item").addClass('grid').children('.product-description').hide();
      list.removeClass('select');
      grid.addClass('select');
    }
  });

$(document).on('click', '.view-switch .list-view', function(event) {
    event.preventDefault();

    $('.product-description').show();
    var list = $(".list-view");
    var grid = $(".grid-view");

    if ( grid.hasClass('select')) {
      $(".product-list-item").removeClass('grid');
      grid.removeClass('select');
      list.addClass('select');
    }
  });
});
