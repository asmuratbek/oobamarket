import React from 'react';
import ReactDOM from 'react-dom';
import createClass from 'create-react-class';
import Product from './components/Product';
import SearchForm from './components/SearchForm';
import CategoryList from './components/CategoryList';
import ProductsCount from './components/ProductsCount';
import axios from 'axios';



var MainInterface = createClass({
  displayName: 'MainInterface',

  getInitialState: function(){
    return {
      products: []
    }
  },

  componentDidMount() {
  axios.get(`http://localhost:8000/product/api/?limit=10`)
    .then(res => {
      const products = res.data.results.map(obj => obj);
      console.log(products)
      this.setState({
         products: products
       });
    });
  },

  render: function() {
    var filteredProducts = [];

    // filteredApts = _.orderBy(filteredApts, function(item) {
    //   return item[orderBy].toLowerCase();
    // }, orderDir);//orderBy

    filteredProducts = this.state.products.map(function(item, index) {
      return(
        <Product key = { index }
          product = { item } />
      ) //return
    }.bind(this));

    return (
      <div>
      <ProductsCount />
      <CategoryList />
      <SearchForm />
      {filteredProducts}
      </div>
    )
  }
});

ReactDOM.render(<MainInterface />, document.getElementById('container'));
