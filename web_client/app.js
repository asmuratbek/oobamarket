var React = require('react')
var ReactDOM = require('react-dom')
var createClass = require('create-react-class')

var Hello = createClass ({
    displayName: 'MyComponent',
    render: function() {
        return (
            <h1>
            Hello, React!
            </h1>
        )
    }
})

ReactDOM.render(<Hello />, document.getElementById('container'))
