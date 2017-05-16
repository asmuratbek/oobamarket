var React = require('react');
var ReactDOM = require('react-dom');
var CreateClass = require('create-react-class');

var Hello = CreateClass ({
    render: function() {
        return (
            <h1>
            Hello, React!
            </h1>
        )
    }
})

ReactDOM.render(<Hello />, document.getElementById('container'))
