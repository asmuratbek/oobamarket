import React, { Component } from 'react'

class List extends Component {

   state = {
       articles: []
   };

   async loadArticles() {
       this.setState({
           articles: await fetch("/api/product/").then(response =>response.json())
       })
   }

   componentWillMount() {
       this.loadArticles();
   }

   render(){
       return(
           <ul className="content-list">
               {this.state.articles.map((article, index) => (
                   <li className="content-list__item" key={index}>
                       {this.state.articles}
                       {article.title}
                   </li>
               ))}
           </ul>
       );
   }
}


export default List
