var React = require('react');
var ReactDOM = require('react-dom');
var createClass = require('create-react-class');

var Hello = createClass ({
    displayName: 'MyComponent',
    render: function() {
        return (
            <div>
                <h1>Yep</h1>
            </div>
        )
    }
});

ReactDOM.render(<Hello />, document.getElementById('container'));
