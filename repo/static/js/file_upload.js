$(function () {

    var tpl = function (i) {
        return '' +
            '<fieldset>' +
            '   <legend>File</legend>' +
            '   <div id="div_id_file-' + i + '-file" class="form-group">' +
            '       <label for="id_file-' + i + '-file" class="control-label requiredField">File</label>' +
            '       <div class="controls">' +
            '           <input class="clearablefileinput" id="id_file-' + i + '-file" name="file-'+ i + '-file" type="file">' +
            '       </div>' +
            '   </div>' +
            '</fieldset>' +
            '<input id="id_file-' + i + '-id" name="file-' + i + '-id" type="hidden">';
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
