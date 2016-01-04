$(function() {
    // look for the namespace form
    var $namespaceSelect = $('#div_id_namespace select');
    var $namespaceClicky = $('<div class="namespace-fancy-select"></div>');
    $namespaceSelect.find('option').each(function() {
        var $namespaceOption = $(this);
        var $fancyOption = $('<div class="namespace-option"><div class="avatar-container namespace-option-avatar"><img src="" class="avatar"></div><span class="namespace-option-name"></span></div>');
        $fancyOption.find('img').attr('src', $namespaceOption.data('avatar'));
        $fancyOption.find('span').text($namespaceOption.text());
        $namespaceClicky.append($fancyOption);
        if ($namespaceOption.attr('selected')) {
            $fancyOption.addClass('namespace-option-selected');
        }

        $fancyOption.click(function() {
            $namespaceClicky.find('.namespace-option-selected').removeClass('namespace-option-selected');
            $fancyOption.addClass('namespace-option-selected');
            $namespaceSelect.val($namespaceOption.attr('value'));
        })
    });
    $('#div_id_namespace').after($namespaceClicky);
    $namespaceSelect.addClass('hide').after($namespaceClicky);
});