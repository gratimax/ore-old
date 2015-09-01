$(function () {
  var logo = $('.logo');
  var logoText = $('.logo-text');

  // logo animation
  logo
    .animate({opacity: 1, top: '0px'}, 800, 'easeOutQuad');

  // logo text animation
  logoText
    .delay(600)
    .animate({opacity: 1}, 300);

  var top = $('.navbar').offset().top;

  var $window = $(window);

  $window.on('scroll', function () {
    if ($window.scrollTop() > top) {
      $('.navbar').addClass('fixed');
      $('.hero').addClass('navbar-fixed');
    } else {
      $('.navbar').removeClass('fixed');
      $('.hero').removeClass('navbar-fixed');
    }
  });

});
