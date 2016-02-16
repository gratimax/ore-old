(function() {
    var markdownIt = require('markdown-it')('commonmark');
    var markdownItEmoji = require('markdown-it-emoji');
    var sanitizeHtml = require('sanitize-html');

    markdownIt.use(markdownItEmoji);

    markdownIt.renderer.rules.emoji = function(token, idx) {
        var m = token[idx].markup;
        return '<img src="//cdn.spongepowered.org/images/emoji/emoji_one/'+m+'.png?v=1" title=":'+m+':" class="emoji" alt=":'+m+':">';
    };

    var renderMarkdown = function renderMarkdown(txt, options) {
        var output = markdownIt.render(txt, options);

        output = sanitizeHtml(output, {
            allowedTags: ['pre', 'code', 'ul', 'ol', 'li', 'p', 'blockquote', 'hr', 'em', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'img', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'caption', 'strike', 'b', 'u', 'i'],
            allowedAttributes: {
                a: ['href', 'name', 'target'],
                img: ['src', 'title', 'alt', 'class', 'width', 'height'],
            },
            transformTags: {
                'img': function(tagName, attribs) {
                    var newAttribs = {};

                    var allowedAttribs = ['src', 'title', 'alt'];
                    for (var i = 0; i < allowedAttribs.length; i++) {
                        var allowedAttrib = allowedAttribs[i];
                        if (!attribs.hasOwnProperty(allowedAttrib)) {
                            continue;
                        }

                        newAttribs[allowedAttrib] = attribs[allowedAttrib];
                    }

                    if (attribs.class && attribs.class === 'emoji') {
                        newAttribs.class = 'emoji';
                    }

                    if (newAttribs.src.indexOf('/uploads/default/') === 0) {
                        // this is a forums.spongepowered.org image
                        // so we'll prepend it with the forums image root
                        newAttribs.src = '//cdn.spongepowered.org' + newAttribs.src;
                    }

                    // check width and height are in bounds, IF explicitly specified
                    if (attribs.hasOwnProperty('width')) {
                        newAttribs.width = Math.max(1, Math.min(920, ~~attribs.width));
                    }
                    if (attribs.hasOwnProperty('height')) {
                        newAttribs.height = Math.max(1, Math.min(600, ~~attribs.height));
                    }

                    return {
                        tagName: 'img',
                        attribs: newAttribs
                    };
                },
            }
        });

        return output;
    };

    if (typeof window !== 'undefined') {
        window.markdown = renderMarkdown;
    }

    if (typeof module !== 'undefined') {
        module.exports = renderMarkdown;
    }

    return renderMarkdown;
})();
