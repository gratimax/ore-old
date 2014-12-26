$(function () {

  var toggled;

  var drop = function () {
    if(toggled) {
      var $toggled = $(toggled);
      $toggled
        .removeClass('dropped')
        .find('.dropdown')
          .css('display', 'none');
    }
  };

  var show = function () {
    if(toggled) {
      var $toggled = $(toggled);
      $toggled
        .addClass('dropped')
        .find('.dropdown')
          .css('display', 'block');
    }
  };

  $('.dropdown-menu')
    .on('click', function (e) {
      e.stopPropagation();
      if (toggled === this) {
        drop();
        toggled = null;
      } else {
        drop();
        toggled = this;
        show();
      }
    })
    .on('click', function () {
      if(toggled && toggled !== this) {
        drop();
        toggled = this;
        show();
      }
    });

  $('html').on('click', function () {
    drop();
    toggled = null;
  })

});
