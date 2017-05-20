// var React = require('react');
// var ReactDOM = require('react-dom');
var createClass = require('create-react-class');
// import List from "./List.";
//
// var Hello = createClass ({
//     displayName: 'MyComponent',
//     render: function() {
//         return (
//             <div>
//                 <h1>Yep</h1>
//                 <List />
//             </div>
//         )
//     }
// })
//
// ReactDOM.render(<Hello />, document.getElementById('container'));


var React = require('react')
var ReactDOM = require('react-dom')

var BooksList = createClass({
    async loadArticles() {
       this.setState({
           articles: await fetch("/api/product/").then(response =>response.json())
       })
   },

   componentWillMount() {
       this.loadArticles();
   },
    render: function() {
        if (this.state.articles) {
            console.log(this.state.articles);
            console.log('DATA!')
            var bookNodes = this.state.data.results.map(function(book){
                return <li> {book.title} </li>
            })
        }
        return (
            <div>
                <h1>Hello React!</h1>
                <ul>
                    {bookNodes}
                </ul>
            </div>
        )
    }
})

ReactDOM.render(<BooksList url='/api/product/' pollInterval={1000} />,
    document.getElementById('container'))
