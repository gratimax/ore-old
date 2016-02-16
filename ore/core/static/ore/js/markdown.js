(function() {
    var hljs = require('highlightjs/highlight.pack.min.js');
    var markdownIt = require('markdown-it')('commonmark', {
        highlight: function(code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return hljs.highlight(lang, code).value;
                } catch (e) {
                    console.error(':(', e);
                }
            }

            return '';
        }

    });
    var markdownItEmoji = require('markdown-it-emoji');
    var sanitizeHtml = require('sanitize-html');

    markdownIt.use(markdownItEmoji);

    markdownIt.renderer.rules.emoji = function(token, idx) {
        var m = token[idx].markup;
        return '<img src="//cdn.spongepowered.org/images/emoji/emoji_one/'+m+'.png?v=1" title=":'+m+':" class="emoji" alt=":'+m+':">';
    };

    var renderMarkdown = function renderMarkdown(txt, options) {
        var output = markdownIt.render(txt);

        var validHljs = ["hljs-addition", "hljs-attr", "hljs-attribute", "hljs-built", "hljs-builtin", "hljs-bullet", "hljs-class", "hljs-comment", "hljs-deletion", "hljs-doctag", "hljs-emphasis", "hljs-keyword", "hljs-link", "hljs-literal", "hljs-meta", "hljs-name", "hljs-number", "hljs-quote", "hljs-regexp", "hljs-section", "hljs-selector", "hljs-string", "hljs-strong", "hljs-subst", "hljs-symbol", "hljs-tag", "hljs-template", "hljs-title", "hljs-type", "hljs-variable"];
        output = sanitizeHtml(output, {
            allowedTags: ['pre', 'code', 'ul', 'ol', 'li', 'p', 'blockquote', 'hr', 'em', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'img', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'caption', 'strike', 'b', 'u', 'i', 'span'],
            allowedAttributes: {
                a: ['href', 'name', 'target'],
                img: ['src', 'title', 'alt', 'class', 'width', 'height'],
                span: ['class'],
            },
            transformTags: {
                'span': function(tagName, attribs) {
                    var newAttribs = {};
                    if (attribs.hasOwnProperty('class') && validHljs.indexOf(attribs.class) !== -1) {
                        newAttribs.class = attribs.class;
                    }

                    return {
                        tagName: tagName,
                        attribs: newAttribs,
                    };
                },
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
