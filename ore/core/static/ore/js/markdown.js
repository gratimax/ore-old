(function() {
    var markdownIt = require('markdown-it')('commonmark');
    var markdownItEmoji = require('markdown-it-emoji');

    markdownIt.use(markdownItEmoji);

    markdownIt.renderer.rules.emoji = function(token, idx) {
        var m = token[idx].markup;
        return '<img src="//cdn.spongepowered.org/images/emoji/emoji_one/'+m+'.png?v=1" title=":'+m+':" class="emoji" alt=":'+m+':">';
    };

    if (window) {
        window.markdown = markdownIt;
    }

    return markdownIt;
})();