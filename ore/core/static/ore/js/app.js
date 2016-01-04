(function () {
    // taken from https://docs.djangoproject.com/en/dev/ref/csrf/#ajax

    var csrfSafeMethod = function (method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    var csrftoken = "{{ csrf_token }}";

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

})();

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

  /**
   * This provides a "croppable" form, where a modal dialog
   * is displayed if the image provided is not of a certain aspect ratio.
   * It looks for elements with the class js-crop-field, and expects
   * to find the following:
   *
   *  - data-width-field should be selector of the crop-width input
   *  - data-height-field should be selector of the crop-height input
   *  - data-x-field should be selector of the crop-x input
   *  - data-y-field should be selector of the crop-x input
   *  - data-aspect-ratio should be width/height
   *  - data-max-width should be max width
   *  - data-max-height should be max height
   *
   * Note that the actual cropping itself is performed server-side - no
   * cropping is actually done on the client, and the entire image is still
   * transferred (at the moment).
   */
   $('.js-crop-field').each(function () {
    var $avatar = $(this);
    var $form = $avatar.closest('form');
    var $inputs = {
      width: $form.find($avatar.data('width-field')),
      height: $form.find($avatar.data('height-field')),
      x: $form.find($avatar.data('x-field')),
      y: $form.find($avatar.data('y-field')),
    };
    var $formGroup = $avatar.closest('.form-group');
    var $err = null;
    var $cropperDiv = null;
    var avatarImg = null;
    var desiredAspectRatio = (+$avatar.data('aspect-ratio')) || 1;
    var maxWidth = ~~$avatar.data('max-width') || null;
    var maxHeight = ~~$avatar.data('max-height') || null;

    $avatar.change(function() {
      var avatarFile, avatarImg;
      if (!(avatarFile = $avatar.get()[0].files[0])) {
        // blergh
        return;
      }

      if ($err) {
        $err.detach();
        $err = null;
      }
      if ($formGroup.hasClass('has-error')) {
        $formGroup.removeClass('has-error');
      }

      if (avatarImg) {
        $(avatarImg).cropper('destroy');
        avatarImg = null;
      }

      if (!$cropperDiv) {
        $cropperDiv = $('<div></div>');
        $avatar.after($cropperDiv);
      } else {
        $cropperDiv.empty();
      }

      avatarImg = new Image();
      avatarImg.onload = function() {
        if ((maxWidth && avatarImg.width > maxWidth) || (maxHeight && avatarImg.height > maxHeight)) {
          var err = 'This image is too large - images can be at most 800x800 pixels.';
          $cropperDiv.empty();
          $formGroup.addClass('has-error');
          $err = $('<span class="help-block"><strong>' + err + '</strong></span>');
          $avatar.after($err);
          avatarImg = null;
          return;
        }

        $cropperDiv.append(avatarImg);
        $(avatarImg).cropper({
          aspectRatio: desiredAspectRatio,
          movable: false,
          scalable: false,
          zoomable: false,
          rotatable: false,
          viewMode: 1,
          crop: function(ev) {
            $inputs.width.val(Math.round(ev.width));
            $inputs.height.val(Math.round(ev.height));
            $inputs.x.val(Math.round(ev.x));
            $inputs.y.val(Math.round(ev.y));
          }
        });
      };
      avatarImg.src = window.URL.createObjectURL(avatarFile);

    });
   });
});
