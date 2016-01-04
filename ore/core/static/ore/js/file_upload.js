$(function () {

    var performReplacement = function(newVal) {
        for (var i = 0; i < this.attributes.length; i++) {
            var attr = this.attributes[i];
            attr.value = attr.value.replace(/-0-/g, '-' + newVal + '-');
        }
        if (this.tagName.toUpperCase() == 'LABEL') {
            this.childNodes[0].textContent = 'Additional file';
        }
        for (var i = 0; i < this.children.length; i++) {
            performReplacement.call(this.children[i], newVal);
        }
    };

    var tpl = function (i) {
        i = ~~i;

        // look for div_id_file-0-file and work upwards
        var $fieldset = $('#div_id_file-0-file').closest('.form-group').clone(false);
        performReplacement.call($fieldset[0], i);
        var $div = $("<div></div>");
        $div.append($fieldset);
        $div.append('<input id="id_file-' + i + '-id" name="file-' + i + '-id" type="hidden">');
        console.log($fieldset, $div);
        return $div.html();
    };

    var next_file = function (i) {
        $('#id_file-' + (i - 1) + '-file').on('change', function () {
            if(!$('#id_file-' + i + '-file').length) {
                console.log($('#id_file-TOTAL_FORMS').val());
                $('#id_file-TOTAL_FORMS').val(i + 1);
                $(tpl(i)).insertAfter($('#id_file-' + (i - 1) + '-id'));
                next_file(i + 1);
            }
        })
    };

    next_file(1);


});
