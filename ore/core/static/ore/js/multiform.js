var setupFormset = function($obj, formPrefix, $addButton) {
    var replaceTagDash = "REPLACETAG-";
    var formPrefixDash = formPrefix + '-';

    var $currentCountEl = $('#id_' + formPrefixDash + 'TOTAL_FORMS');
    var currentCount = parseInt($currentCountEl.val(), 10);

    var $maxCountEl = $('#id_' + formPrefixDash + 'MAX_NUM_FORMS');
    var maxCount = parseInt($maxCountEl.val(), 10);

    var replacomatic = function($baseEl, from, to) {
        var $myEl = $baseEl.clone();
        var replaceInAttrs = ['name', 'id', 'for'];
        $myEl.find('*').each(function(_, el) {
            var $el = $(el);
            replaceInAttrs.forEach(function(attrName) {
                var value = $el.attr(attrName);
                console.log(attrName, value, el);
                if (value !== undefined) {
                    var value = $el.attr(attrName);
                    if (value.indexOf(from) !== -1) {
                        value = value.replace(from, to);
                        $el.attr(attrName, value);
                    }
                }
            });

            if ($el.attr('value') !== undefined) {
                $el.attr('value', '');
            }
        });
        return $myEl;
    };

    var innerFormset = replacomatic($obj, formPrefixDash + '0-', replaceTagDash);

    $addButton.click(function() {
        if (currentCount >= maxCount) return;

        $obj.parent().append(replacomatic(innerFormset, replaceTagDash, formPrefixDash + currentCount + '-'));

        currentCount++;
        $currentCountEl.val(currentCount);
        return false;
    });
};
