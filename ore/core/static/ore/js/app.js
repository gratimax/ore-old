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

  /**
   * This provides a "lockable" form, which disables button(s) until a
   * certain input is provided. It looks for elements with the class
   * js-lock-form, and expects to find the following properties:
   *
   *  - data-confirm should be the string you want the user to verify.
   *  - data-input should be the input box to "watch" for verification.
   *  - data-locks should be elements which are disabled until the
   *               input value matches the confirmation.
   *
   */
  $('.js-lock-form').each(function () {
    var $form = $(this);
    var $input = $form.find($form.data('input'));
    var $locks = $form.find($form.data('locks'));
    var confirm = $form.data('confirm');

    function checkLock () {
      $locks.prop('disabled', $input.val() !== confirm);
    }

    $input.on('input', checkLock);
    checkLock();
  });

  $(function () {
    $('[data-toggle="tooltip"]').tooltip({
      container: 'body'
    })
  });
});
