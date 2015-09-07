window.notify = function (options) {
  if (options.style == 'top_sticky') {
    if ($("#top-sticky-notification").length == 0) {
      // Add element if not exists
      var element = document.createElement("div");
      element.id = 'top-sticky-notification';
      $("body").append(element);
    }

    $('#top-sticky-notification')
      .html(options.message)
      .slideDown(300, function() {
        setTimeout( function () {
          $('#top-sticky-notification').slideUp(300);
        }, 3000);
      });
  }
};
