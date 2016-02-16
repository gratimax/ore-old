var express = require('express');
var bodyParser = require('body-parser');

var markdown = require('../core/static/ore/js/markdown');
var app = express();

app.use(bodyParser.json());

app.post('/markdown-it', function (req, res) {
    var input = req.body.input;
    res.send(markdown(input));
});

app.listen(3001);

console.log('markdown server started on port 3001');